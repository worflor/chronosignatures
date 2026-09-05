"""
CHRONOSIGNATURES (Annex): "What B Was For"
Bonus track by Claude Sonnet 5, closing out 09 and 10. Track 09's final chord
borrows a B natural outside G harmonic minor; Track 10 (E Phrygian) has that same
B as its dominant. This piece modulates between the two.

Three sections in one file:
- Part A (G harmonic minor, 7/8, 63 BPM): reprise of 09's two opposed waveguide
  voices, drifting into alignment.
- Bridge (~11s, no meter): the shared B note held and granulated.
- Part B (E Phrygian, 4/4, 76 BPM): 09's voices now play in unison; the vocal
  phrase left unresolved in 10 finally resolves to the tonic.

No mid-song meter/tempo change exists in the Score IR (HARMONIA_WISHLIST.md item 8),
so Part A/B are compiled as separate Scores at matched loudness and stitched with
the Bridge via crossfades.
"""

import os
import subprocess
import shutil
import numpy as np
import scipy.io.wavfile as wavfile
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON, TCOP, COMM

from harmonia.ir.schema import (
    Score, ChordDef, MacroBlock, MasteringConfig, VoicePocketConfig, TrackChannel, SendBusDef, FXDef, NoteEvent
)
from harmonia.ir.parser import ScoreParser
from harmonia.tools.api import HarmoniaStudio
from harmonia.dsp.synths.formant_vocal import FormantVocaloidSynth
from harmonia.dsp.synths.waveguide import DigitalWaveguideStringSynth
from harmonia.dsp.synths.granular import CloudGranularSynth
from harmonia.dsp.primitives import StudioConvolutionReverb, apply_tpdf_dither, add_to_track
from harmonia.mixer.mastering import BroadcastMasteringEngine
from harmonia.mixer.voice_pocket import VoicePocketProcessor
from harmonia.generative.determinism import content_fingerprint

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACK_DIR = os.path.join(REPO_ROOT, "tracks")
ART_DIR = os.path.join(REPO_ROOT, "art")
SR = 44100
SHARED_LUFS = -17.5

PART_A_BPM = 63.0
PART_A_QNPB = 3.5  # 7/8
PART_A_BEAT_S = 60.0 / PART_A_BPM

PART_B_BPM = 76.0
PART_B_QNPB = 4.0  # 4/4
PART_B_BEAT_S = 60.0 / PART_B_BPM


# ---------------------------------------------------------------------------
# Part A: G harmonic minor, 7/8 -- reprise of Track 09, drifting into alignment
# ---------------------------------------------------------------------------

def build_part_a() -> Score:
    chords = [
        ChordDef("Gm(maj9)", bass_midi=43,
                 pad_notes=[55, 58, 62, 66, 69], stab_notes=[58, 62, 66],
                 bell_notes=[62, 66, 69, 74], vocal_notes=[74, 69]),
        ChordDef("Cm9", bass_midi=48,
                 pad_notes=[60, 63, 67, 70, 74], stab_notes=[63, 67, 70],
                 bell_notes=[67, 70, 74, 79], vocal_notes=[79, 74]),
        ChordDef("D7", bass_midi=50,
                 pad_notes=[54, 57, 60, 62, 66], stab_notes=[57, 60, 62],
                 bell_notes=[60, 62, 66, 69], vocal_notes=[69, 66]),
        ChordDef("Ebmaj7#5", bass_midi=51,
                 pad_notes=[63, 67, 71, 74, 79], stab_notes=[67, 71, 74],
                 bell_notes=[71, 74, 79, 82], vocal_notes=[82, 79]),
    ]

    timeline = [
        MacroBlock("1_Approach", "MAIN", num_bars=8, energy=0.45,
                   has_drums=False, has_bass=False, has_pad=True, has_stabs=False,
                   has_bells=True, has_vocaloid=False, filter_cutoff=750.0,
                   groove_profile="bossa_drift"),
        MacroBlock("2_Nearing_Alignment", "MAIN", num_bars=6, energy=0.60,
                   has_drums=False, has_bass=False, has_pad=True, has_stabs=False,
                   has_bells=True, has_vocaloid=False, filter_cutoff=900.0,
                   groove_profile="bossa_drift"),
    ]
    total_bars = sum(b.num_bars for b in timeline)

    motif_fwd = [0, 1, 2, 3]
    motif_rev = [3, 2, 1, 0]
    converge_bars = 2  # last N bars: reversed voice snaps to the forward note

    fwd_events, rev_events = [], []
    for bar in range(total_bars):
        chord = chords[bar % len(chords)]
        b_start = bar * PART_A_QNPB
        fwd_note = chord.pad_notes[motif_fwd[bar % len(motif_fwd)] % len(chord.pad_notes)]
        if bar >= total_bars - converge_bars:
            rev_note = fwd_note
        else:
            rev_note = chord.pad_notes[motif_rev[bar % len(motif_rev)] % len(chord.pad_notes)]
        drift_t = bar / max(1, total_bars - 1)
        rev_pan = 0.40 * (1.0 - drift_t) + 0.05 * drift_t
        fwd_events.append(NoteEvent(start_beat=b_start, duration_beats=PART_A_QNPB * 0.92,
                                     midi_note=fwd_note, velocity=0.55, pan=-0.35))
        rev_events.append(NoteEvent(start_beat=b_start, duration_beats=PART_A_QNPB * 0.92,
                                     midi_note=rev_note, velocity=0.50, pan=rev_pan))

    fwd_channel = TrackChannel(id="string_fwd", instrument_id="waveguide", events=fwd_events,
                                fx_chain=[FXDef(plugin_type="filter", params={"cutoff_hz": 5200.0, "mode": "lowpass"})],
                                sends={"chamber_verb": 0.42}, volume_db=-2.0, pan=-0.35)
    rev_channel = TrackChannel(id="string_rev", instrument_id="waveguide", events=rev_events,
                                fx_chain=[FXDef(plugin_type="filter", params={"cutoff_hz": 4600.0, "mode": "lowpass"})],
                                sends={"chamber_verb": 0.48}, volume_db=-2.8, pan=0.0)

    granular_events = []
    for bar in range(0, total_bars, 2):
        chord = chords[bar % len(chords)]
        b_start = bar * PART_A_QNPB
        for note in [chord.bass_midi + 12, chord.pad_notes[-1]]:
            granular_events.append(NoteEvent(start_beat=b_start, duration_beats=PART_A_QNPB * 2.1,
                                              midi_note=note, velocity=0.28 + 0.12 * (bar / total_bars), pan=0.0))
    granular_channel = TrackChannel(id="granular_atmosphere", instrument_id="granular", events=granular_events,
                                     fx_chain=[FXDef(plugin_type="dimension", params={"width": 1.9, "hp_side_hz": 220.0})],
                                     sends={"chamber_verb": 0.60}, volume_db=-4.0, pan=0.0)

    acid_events = []
    for bar in range(total_bars):
        chord = chords[bar % len(chords)]
        b_start = bar * PART_A_QNPB
        acid_events.append(NoteEvent(start_beat=b_start, duration_beats=PART_A_QNPB * 0.85,
                                      midi_note=chord.bass_midi - 12,
                                      velocity=0.45 + 0.35 * (bar / total_bars), pan=0.0))
    acid_channel = TrackChannel(id="acid_undertow", instrument_id="acid_bass", events=acid_events,
                                 fx_chain=[FXDef(plugin_type="filter", params={"cutoff_hz": 380.0, "resonance": 1.6, "mode": "lowpass"}),
                                           FXDef(plugin_type="distortion", params={"drive": 1.3, "mode": "diode", "tone": 0.45}, mix=0.35)],
                                 sends={"undertow_room": 0.30}, volume_db=-2.5, pan=0.0)

    send_busses = {
        "chamber_verb": SendBusDef(id="chamber_verb", fx_chain=[
            FXDef(plugin_type="reverb", params={"decay_time_s": 4.6, "damp_hz": 3800.0}, mix=1.0),
            FXDef(plugin_type="dimension", params={"width": 1.7, "hp_side_hz": 200.0}),
        ], volume_db=-4.5),
        "undertow_room": SendBusDef(id="undertow_room", fx_chain=[
            FXDef(plugin_type="reverb", params={"decay_time_s": 1.6}, mix=0.6),
        ], volume_db=-6.0),
    }

    return Score(
        title="11a What B Was For (Approach)",
        schema_version="2.3", seed=111011,
        bpm=PART_A_BPM, meter_numerator=7, meter_denominator=8,
        key_root="G", scale_type="harmonic_minor", groove_profile="bossa_drift", swing_ratio=0.52,
        chords={"MAIN": chords}, timeline=timeline,
        track_channels=[fwd_channel, rev_channel, granular_channel, acid_channel],
        send_busses=send_busses,
        master_bus_fx=[FXDef(plugin_type="dimension", params={"width": 1.25, "hp_side_hz": 190.0})],
        mastering=MasteringConfig(target_lufs=SHARED_LUFS, peak_ceiling_db=-1.2, tape_warmth_enabled=True,
                                   fade_in_s=1.5, fade_out_s=0.3,
                                   voice_pocket=VoicePocketConfig(enabled=True, center_freq_hz=2400.0, gain_db=-3.2)),
        metadata={"track_number": "11a", "bonus_track": True}
    )


# ---------------------------------------------------------------------------
# Bridge: ~11s, no meter -- the B natural held and granulated
# ---------------------------------------------------------------------------

def render_bridge() -> np.ndarray:
    dur_s = 11.0
    waveguide = DigitalWaveguideStringSynth(sr=SR)
    granular = CloudGranularSynth(sr=SR)

    tone_lo = waveguide.render_pluck(midi_note=59, duration_s=dur_s, velocity=0.55, brightness=0.45, decay_factor=0.998)
    tone_hi = waveguide.render_pluck(midi_note=71, duration_s=dur_s, velocity=0.40, brightness=0.55, decay_factor=0.997)
    cloud = granular.render_note(midi_note=71, duration_s=dur_s, velocity=0.55)

    n = min(len(tone_lo), len(tone_hi), len(cloud))
    mix = tone_lo[:n] * 1.0 + tone_hi[:n] * 0.7 + cloud[:n] * 1.0

    reverb = StudioConvolutionReverb(sr=SR, decay_time_s=5.5, damp_hz=3000.0)
    wet = reverb.process(mix, mix=0.55)

    peak = np.max(np.abs(wet)) + 1e-9
    wet = wet / peak * 0.42  # sit quietly under the surrounding sections, a hush

    fade_len = int(1.5 * SR)
    if len(wet) > 2 * fade_len:
        wet[:fade_len] *= np.linspace(0.0, 1.0, fade_len)[:, None]
        wet[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)[:, None]
    return wet.astype(np.float32)


# ---------------------------------------------------------------------------
# Part B: E Phrygian, 4/4 -- Track 10's chords return, the vocal finishes its line
# ---------------------------------------------------------------------------

def build_part_b() -> Score:
    chords = [
        ChordDef("Em7(b9 color)", bass_midi=40,
                 pad_notes=[52, 55, 59, 62], stab_notes=[52, 55, 59, 62],
                 bell_notes=[59, 62, 65, 71], vocal_notes=[64, 59]),
        ChordDef("Fmaj7", bass_midi=41,
                 pad_notes=[53, 57, 60, 64], stab_notes=[53, 57, 60, 64],
                 bell_notes=[60, 64, 65, 69], vocal_notes=[65, 60]),
        ChordDef("Am7", bass_midi=45,
                 pad_notes=[57, 60, 64, 67], stab_notes=[57, 60, 64, 67],
                 bell_notes=[64, 67, 69, 72], vocal_notes=[69, 64]),
        ChordDef("Bm7b5", bass_midi=47,
                 pad_notes=[59, 62, 65, 69], stab_notes=[59, 62, 65, 69],
                 bell_notes=[65, 69, 71, 74], vocal_notes=[71, 65]),
    ]

    rhythm_whisper = {
        "kick":  [0] * 16, "snare": [0] * 16,
        "hat":   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    }

    timeline = [
        MacroBlock("1_Arrival", "MAIN", num_bars=8, energy=0.55,
                   has_drums=False, has_bass=True, has_pad=True, has_stabs=True,
                   has_bells=True, has_vocaloid=False, filter_cutoff=850.0,
                   groove_profile="bossa_drift"),
        MacroBlock("2_Resolution", "MAIN", num_bars=8, energy=0.72,
                   has_drums=True, has_bass=True, has_pad=True, has_stabs=True,
                   has_bells=True, has_vocaloid=False, filter_cutoff=1000.0,
                   groove_profile="bossa_drift", rhythm_patterns=rhythm_whisper),
    ]
    total_bars = sum(b.num_bars for b in timeline)

    motif_fwd = [0, 1, 2, 3]
    string_a_events, string_b_events = [], []
    for bar in range(total_bars):
        chord = chords[bar % len(chords)]
        b_start = bar * PART_B_QNPB
        note = chord.pad_notes[motif_fwd[bar % len(motif_fwd)] % len(chord.pad_notes)]
        string_a_events.append(NoteEvent(start_beat=b_start, duration_beats=PART_B_QNPB * 0.9,
                                          midi_note=note, velocity=0.45, pan=-0.22))
        string_b_events.append(NoteEvent(start_beat=b_start, duration_beats=PART_B_QNPB * 0.9,
                                          midi_note=note, velocity=0.42, pan=0.22))

    string_a_channel = TrackChannel(id="string_unison_a", instrument_id="waveguide", events=string_a_events,
                                     fx_chain=[FXDef(plugin_type="filter", params={"cutoff_hz": 5200.0, "mode": "lowpass"})],
                                     sends={"chamber_verb": 0.40}, volume_db=-3.0, pan=-0.22)
    string_b_channel = TrackChannel(id="string_unison_b", instrument_id="waveguide", events=string_b_events,
                                     fx_chain=[FXDef(plugin_type="filter", params={"cutoff_hz": 5000.0, "mode": "lowpass"})],
                                     sends={"chamber_verb": 0.40}, volume_db=-3.0, pan=0.22)

    send_busses = {
        "chamber_verb": SendBusDef(id="chamber_verb", fx_chain=[
            FXDef(plugin_type="reverb", params={"decay_time_s": 4.2, "damp_hz": 3600.0}, mix=1.0),
            FXDef(plugin_type="dimension", params={"width": 1.6, "hp_side_hz": 200.0}),
        ], volume_db=-4.5),
    }

    return Score(
        title="11b What B Was For (Resolution)",
        schema_version="2.3", seed=111012,
        bpm=PART_B_BPM, meter_numerator=4, meter_denominator=4,
        key_root="E", scale_type="phrygian", groove_profile="bossa_drift", swing_ratio=0.50,
        chords={"MAIN": chords}, timeline=timeline,
        track_channels=[string_a_channel, string_b_channel],
        send_busses=send_busses,
        master_bus_fx=[],
        mastering=MasteringConfig(target_lufs=SHARED_LUFS, peak_ceiling_db=-1.2, tape_warmth_enabled=True,
                                   fade_in_s=0.5, fade_out_s=6.0,
                                   voice_pocket=VoicePocketConfig(enabled=True, center_freq_hz=2400.0, gain_db=-3.2)),
        metadata={"track_number": "11b", "bonus_track": True, "keys_synth": "rhodes"}
    )


def build_resolution_vocal_phrases():
    # Picks up exactly where Track 10 left off (...A-G-F, unresolved) and finishes it: F -> E (tonic), held.
    return [
        (32.0, [(67, 2.0), (65, 2.0)]),
        (48.0, [(69, 1.0), (67, 1.0), (65, 2.0), (64, 6.0)]),
    ]


def render_part_b_vocal(total_samples: int) -> np.ndarray:
    synth = FormantVocaloidSynth(sr=SR)
    reverb = StudioConvolutionReverb(sr=SR, decay_time_s=4.2, damp_hz=3400.0)
    vocal_track = np.zeros((total_samples, 2), dtype=np.float32)
    for start_beat, notes_durs in build_resolution_vocal_phrases():
        notes = [n for n, _ in notes_durs]
        durs_s = [d * PART_B_BEAT_S for _, d in notes_durs]
        phrase_audio = synth.render_legato_phrase(notes, durs_s, vowel='o', velocity=0.72, glide_s=0.11)
        start_sample = int(start_beat * PART_B_BEAT_S * SR)
        add_to_track(vocal_track, start_sample, phrase_audio)
    return reverb.process(vocal_track, mix=0.36)


def crossfade_concat(a: np.ndarray, b: np.ndarray, fade_s: float) -> np.ndarray:
    fade_n = int(fade_s * SR)
    fade_n = min(fade_n, len(a) // 2, len(b) // 2)
    if fade_n <= 0:
        return np.concatenate([a, b], axis=0)
    fade_out = np.linspace(1.0, 0.0, fade_n, dtype=np.float32)[:, None]
    fade_in = np.linspace(0.0, 1.0, fade_n, dtype=np.float32)[:, None]
    head = a[:-fade_n]
    overlap = a[-fade_n:] * fade_out + b[:fade_n] * fade_in
    tail = b[fade_n:]
    return np.concatenate([head, overlap, tail], axis=0)


def tag_mp3(mp3_path: str, concept: str, art_path: str):
    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass
    audio.tags.add(TIT2(encoding=3, text="What B Was For"))
    audio.tags.add(TPE1(encoding=3, text="Harmonia Engine · Claude"))
    audio.tags.add(TPE2(encoding=3, text="Harmonia Engine · Claude"))
    audio.tags.add(TALB(encoding=3, text="Chronosignatures (Annex)"))
    audio.tags.add(TRCK(encoding=3, text="11"))
    audio.tags.add(TDRC(encoding=3, text="2026"))
    audio.tags.add(TCON(encoding=3, text="Ambient / Neo-Classical"))
    audio.tags.add(TCOP(encoding=3, text="© 2026 Harmonia Engine"))
    audio.tags.add(COMM(encoding=3, lang="eng", desc="Description", text=concept))
    art_embedded = False
    if os.path.exists(art_path):
        with open(art_path, "rb") as f:
            audio.tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=f.read()))
        art_embedded = True
    audio.save(v2_version=3)
    print(f"  [ID3 Tagged] {mp3_path} (art embedded: {art_embedded})")


def compile_bonus_track_3():
    prefix = "11_what_b_was_for"
    art_path = os.path.join(ART_DIR, f"{prefix}.jpg")
    studio = HarmoniaStudio()
    print("=== COMPILING BONUS TRACK 3: 'What B Was For' ===")

    score_a = build_part_a()
    score_b = build_part_b()
    ScoreParser.validate(score_a)
    ScoreParser.validate(score_b)
    # Public-facing titles (build_part_a/b use internal "11a"/"11b (...)" labels
    # for their own bookkeeping; these are what ship in the MIDI/MusicXML/JSON).
    score_a.title = "What B Was For (Part A)"
    score_b.title = "What B Was For"

    ScoreParser.save_to_file(score_a, os.path.join(TRACK_DIR, f"{prefix}_partA.json"))
    ScoreParser.save_to_file(score_b, os.path.join(TRACK_DIR, f"{prefix}_partB.json"))

    wav_a_path = os.path.join(TRACK_DIR, f"{prefix}_partA_tmp.wav")
    wav_b_path = os.path.join(TRACK_DIR, f"{prefix}_partB_tmp.wav")

    studio.compile_score(score_a, output_path=wav_a_path, export_mp3=False, export_stems=False,
                          export_midi=False, export_musicxml=False)
    print(f"  Rendered Part A: {wav_a_path}")

    res_b = studio.compile_score(score_b, output_path=wav_b_path, export_mp3=False, export_stems=False,
                                  export_midi=True, export_musicxml=True)
    print(f"  Rendered Part B (instrumental): {wav_b_path}")

    sr_a, data_a = wavfile.read(wav_a_path)
    sr_b, data_b = wavfile.read(wav_b_path)
    assert sr_a == SR and sr_b == SR
    part_a = data_a.astype(np.float32) / 32767.0
    part_b_instrumental = data_b.astype(np.float32) / 32767.0

    vocal = render_part_b_vocal(len(part_b_instrumental))
    if len(vocal) < len(part_b_instrumental):
        vocal = np.pad(vocal, ((0, len(part_b_instrumental) - len(vocal)), (0, 0)))
    else:
        vocal = vocal[:len(part_b_instrumental)]
    # Vocaloid channels normally get a voice-pocket carve; this hand-mixed phrase
    # bypasses that pipeline, so apply it explicitly.
    vocal_carver = VoicePocketProcessor(config=score_b.mastering.voice_pocket, sr=SR)
    vocal = vocal_carver.process(vocal)
    part_b_mixed = part_b_instrumental + vocal * 1.05

    masterer = BroadcastMasteringEngine(config=score_b.mastering, sr=SR)
    part_b = masterer.master(part_b_mixed)
    print("  Mixed and re-mastered Part B with resolving vocal phrase")

    bridge = render_bridge()
    print(f"  Rendered Bridge: {len(bridge) / SR:.2f}s")

    full = crossfade_concat(part_a, bridge, fade_s=0.8)
    full = crossfade_concat(full, part_b, fade_s=0.8)

    dithered = apply_tpdf_dither(full, bit_depth=16, seed=111013)
    int16_out = (np.clip(dithered, -1.0, 1.0) * 32767.0).astype(np.int16)

    out_wav = os.path.join(TRACK_DIR, f"{prefix}.wav")
    wavfile.write(out_wav, SR, int16_out)
    print(f"  Stitched final master -> {out_wav}")

    ffmpeg = shutil.which("ffmpeg")
    out_mp3 = os.path.join(TRACK_DIR, f"{prefix}.mp3")
    subprocess.run([ffmpeg, "-y", "-i", out_wav, "-codec:a", "libmp3lame", "-b:a", "320k", out_mp3],
                    check=True, capture_output=True)
    print(f"  Exported MP3: {out_mp3}")

    # Rename Part B's MIDI/MusicXML to the final track prefix; clean up temp files
    for ext in (".mid", ".musicxml"):
        tmp_path = os.path.splitext(wav_b_path)[0] + ext
        final_path = os.path.join(TRACK_DIR, f"{prefix}{ext}")
        if os.path.exists(tmp_path):
            os.replace(tmp_path, final_path)
    for p in (wav_a_path, wav_b_path):
        if os.path.exists(p):
            os.remove(p)
        manifest_p = os.path.splitext(p)[0] + ".manifest.json"
        if os.path.exists(manifest_p):
            os.remove(manifest_p)

    concept = (
        "The closing bracket for the Annex. Track 09 ended on a chord borrowing a B "
        "natural that didn't belong to its own scale; Track 10 lives in a scale built "
        "on that same B as its dominant. This piece walks through that door: the two "
        "waveguide voices from 09 drift out of opposition into unison, and the vocal "
        "phrase left hanging at the end of 10 is finally allowed to resolve."
    )
    tag_mp3(out_mp3, concept, art_path)

    import hashlib, json as json_lib
    with open(out_wav, "rb") as f:
        render_sha256 = hashlib.sha256(f.read()).hexdigest()
    manifest = {
        "manifest_version": "1.0",
        "engine": "harmonia",
        "structure": "stitched composite: Part A (Score IR) -> hand-synthesized Bridge -> Part B (Score IR)",
        "part_a_score_fingerprint": content_fingerprint(score_a),
        "part_b_score_fingerprint": content_fingerprint(score_b),
        "render_sha256": render_sha256,
        "sample_rate": SR,
        "frames": len(int16_out),
        "channels": 2,
    }
    with open(os.path.join(TRACK_DIR, f"{prefix}.manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json_lib.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")

    acoustic = studio.analyze_audio_file(out_wav)
    print(f"  [Acoustics] LUFS: {acoustic.integrated_lufs_estimate:.2f}, "
          f"Dynamic Range: {acoustic.dynamic_range_db:.2f} dB, "
          f"True Peak: {acoustic.true_peak_dbfs:.2f} dBFS")
    print("=== BONUS TRACK 3 COMPILATION COMPLETE ===")


if __name__ == "__main__":
    compile_bonus_track_3()
