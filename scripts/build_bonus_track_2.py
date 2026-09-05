"""
CHRONOSIGNATURES (Annex): "The Sound Before Language"
Bonus track by Claude Sonnet 5. FormantVocaloidSynth carries the full lead melody
(elsewhere on the album it's only used for short accent notes), sung on held vowels
with no resolution onto the tonic.

Added render_legato_phrase() to harmonia/dsp/synths/formant_vocal.py: a continuous
pitch-glide phrase renderer, since TrackChannel/NoteEvent dispatch has no legato
primitive (HARMONIA_WISHLIST.md item 9). The vocal is synthesized separately and
mixed into the compiled instrumental bed as a manual post-process.
"""

import os
import subprocess
import shutil
import numpy as np
import scipy.io.wavfile as wavfile
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON, TCOP, COMM

from harmonia.ir.schema import (
    Score, ChordDef, MacroBlock, MasteringConfig, VoicePocketConfig
)
from harmonia.ir.parser import ScoreParser
from harmonia.tools.api import HarmoniaStudio
from harmonia.dsp.synths.formant_vocal import FormantVocaloidSynth
from harmonia.dsp.primitives import StudioConvolutionReverb, apply_tpdf_dither, add_to_track
from harmonia.mixer.mastering import BroadcastMasteringEngine
from harmonia.mixer.voice_pocket import VoicePocketProcessor

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACK_DIR = os.path.join(REPO_ROOT, "tracks")
ART_DIR = os.path.join(REPO_ROOT, "art")

BPM = 54.0
SR = 44100
BEAT_S = 60.0 / BPM


def build_score() -> Score:
    # E Phrygian: E F G A B C D (52 53 55 57 59 60 62)
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
        "kick":  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "snare": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "hat":   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    }

    timeline = [
        MacroBlock("1_Intake_Breath", "MAIN", num_bars=8, energy=0.32,
                   has_drums=False, has_bass=True, has_pad=True, has_stabs=True,
                   has_bells=False, has_vocaloid=False, filter_cutoff=650.0,
                   groove_profile="bossa_drift"),
        MacroBlock("2_Reaching", "MAIN", num_bars=8, energy=0.50,
                   has_drums=False, has_bass=True, has_pad=True, has_stabs=True,
                   has_bells=True, has_vocaloid=False, filter_cutoff=800.0,
                   groove_profile="bossa_drift"),
        MacroBlock("3_The_Held_Breath", "MAIN", num_bars=8, energy=0.68,
                   has_drums=True, has_bass=True, has_pad=True, has_stabs=True,
                   has_bells=True, has_vocaloid=False, filter_cutoff=950.0,
                   groove_profile="bossa_drift", rhythm_patterns=rhythm_whisper),
        MacroBlock("4_Unfinished", "MAIN", num_bars=8, energy=0.34,
                   has_drums=False, has_bass=True, has_pad=True, has_stabs=True,
                   has_bells=True, has_vocaloid=False, filter_cutoff=600.0,
                   groove_profile="bossa_drift"),
    ]

    return Score(
        title="10 The Sound Before Language",
        schema_version="2.3",
        seed=101010,
        bpm=BPM,
        meter_numerator=4,
        meter_denominator=4,
        key_root="E",
        scale_type="phrygian",
        groove_profile="bossa_drift",
        swing_ratio=0.50,
        chords={"MAIN": chords},
        timeline=timeline,
        master_bus_fx=[],
        mastering=MasteringConfig(
            target_lufs=-19.0,
            peak_ceiling_db=-1.0,
            tape_warmth_enabled=True,
            fade_in_s=2.0,
            fade_out_s=6.0,
            voice_pocket=VoicePocketConfig(enabled=True, center_freq_hz=2400.0, gain_db=-3.2)
        ),
        metadata={
            "track_number": 10,
            "bonus_track": True,
            "keys_synth": "rhodes",
            "concept": (
                "A wordless torch-song lament. The lead voice is FormantVocaloidSynth "
                "pushed into a role it was never built for -- a full sung phrase rather "
                "than an accent -- and it can only ache through vowels, because that is "
                "genuinely all it can do: no consonants, no words, just formant "
                "resonance. It ends on the Phrygian flat-2, unresolved, mid-sentence."
            )
        }
    )


def build_vocal_phrases():
    """
    Hand-written melody in E Phrygian, grouped into breath-phrases. Each phrase is one
    continuous legato render (glide within), with a fresh breath/attack between phrases.
    Format: (start_beat, [(midi_note, duration_beats), ...])
    """
    return [
        (8.0,  [(64, 2.0), (67, 1.5), (65, 2.5)]),
        (20.0, [(71, 1.0), (69, 1.0), (67, 2.0), (64, 2.0)]),
        (40.0, [(67, 1.0), (69, 1.0), (72, 2.0), (71, 1.5), (69, 2.5)]),
        (56.0, [(74, 1.0), (72, 1.0), (69, 2.0), (65, 3.0)]),
        (72.0, [(77, 1.0), (74, 2.0), (71, 2.0), (67, 3.0)]),
        (96.0, [(69, 2.0), (67, 2.0), (65, 4.0)]),  # ends unresolved on F (Phrygian b2)
    ]


def render_vocal_track(total_samples: int) -> np.ndarray:
    synth = FormantVocaloidSynth(sr=SR)
    reverb = StudioConvolutionReverb(sr=SR, decay_time_s=3.8, damp_hz=3200.0)
    vocal_track = np.zeros((total_samples, 2), dtype=np.float32)

    for start_beat, notes_durs in build_vocal_phrases():
        notes = [n for n, _ in notes_durs]
        durs_s = [d * BEAT_S for _, d in notes_durs]
        phrase_audio = synth.render_legato_phrase(
            notes, durs_s, vowel='o', velocity=0.72, glide_s=0.11
        )
        start_sample = int(start_beat * BEAT_S * SR)
        add_to_track(vocal_track, start_sample, phrase_audio)

    vocal_track = reverb.process(vocal_track, mix=0.38)
    return vocal_track


def mix_and_export(instrumental_wav_path: str, out_prefix: str, score: Score):
    sr, data = wavfile.read(instrumental_wav_path)
    assert sr == SR
    instrumental = data.astype(np.float32) / 32767.0
    total_samples = len(instrumental)

    vocal = render_vocal_track(total_samples)
    if len(vocal) < total_samples:
        vocal = np.pad(vocal, ((0, total_samples - len(vocal)), (0, 0)))
    else:
        vocal = vocal[:total_samples]

    # Vocaloid channels normally get a voice-pocket notch carve via build_default_mixer;
    # this hand-mixed phrase bypasses that pipeline, so apply it explicitly.
    vocal_carver = VoicePocketProcessor(config=score.mastering.voice_pocket, sr=SR)
    vocal = vocal_carver.process(vocal)

    mixed = instrumental + vocal * 1.1

    # Full loudness-targeting + limiting pass (not just a peak limiter), so the mix
    # actually hits the score's target_lufs rather than whatever the peaks land on.
    masterer = BroadcastMasteringEngine(config=score.mastering, sr=SR)
    mastered = masterer.master(mixed)

    dithered = apply_tpdf_dither(mastered, bit_depth=16, seed=101010)
    int16_out = (np.clip(dithered, -1.0, 1.0) * 32767.0).astype(np.int16)

    out_wav = os.path.join(TRACK_DIR, f"{out_prefix}.wav")
    wavfile.write(out_wav, SR, int16_out)
    print(f"  Mixed vocal + instrumental -> {out_wav}")

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg not on PATH")
    out_mp3 = os.path.join(TRACK_DIR, f"{out_prefix}.mp3")
    subprocess.run([ffmpeg, "-y", "-i", out_wav, "-codec:a", "libmp3lame", "-b:a", "320k", out_mp3],
                    check=True, capture_output=True)
    print(f"  Exported MP3: {out_mp3}")
    return out_wav, out_mp3


def tag_mp3(mp3_path: str, score: Score, art_path: str):
    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    audio.tags.add(TIT2(encoding=3, text="The Sound Before Language"))
    audio.tags.add(TPE1(encoding=3, text="Harmonia Engine · Claude"))
    audio.tags.add(TPE2(encoding=3, text="Harmonia Engine · Claude"))
    audio.tags.add(TALB(encoding=3, text="Chronosignatures (Annex)"))
    audio.tags.add(TRCK(encoding=3, text="10"))
    audio.tags.add(TDRC(encoding=3, text="2026"))
    audio.tags.add(TCON(encoding=3, text="Torch Song / Ambient Noir"))
    audio.tags.add(TCOP(encoding=3, text="© 2026 Harmonia Engine"))
    audio.tags.add(COMM(encoding=3, lang="eng", desc="Description", text=score.metadata.get("concept", "")))

    art_embedded = False
    if os.path.exists(art_path):
        with open(art_path, "rb") as img_f:
            audio.tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=img_f.read()))
        art_embedded = True
    audio.save(v2_version=3)
    print(f"  [ID3 Tagged] {mp3_path} (art embedded: {art_embedded})")


def compile_bonus_track_2():
    score = build_score()
    ScoreParser.validate(score)
    prefix = "10_the_sound_before_language"
    art_path = os.path.join(ART_DIR, f"{prefix}.jpg")

    studio = HarmoniaStudio()
    print("=== COMPILING BONUS TRACK 2: 'The Sound Before Language' ===")

    json_path = os.path.join(TRACK_DIR, f"{prefix}.json")
    ScoreParser.save_to_file(score, json_path)
    print(f"  Saved Score IR: {json_path}")

    instrumental_prefix = f"{prefix}_instrumental_tmp"
    instrumental_wav = os.path.join(TRACK_DIR, f"{instrumental_prefix}.wav")
    res = studio.compile_score(
        score, output_path=instrumental_wav,
        export_mp3=False, export_stems=False, export_midi=True, export_musicxml=True
    )
    print(f"  Rendered instrumental bed: {instrumental_wav}")

    out_wav, out_mp3 = mix_and_export(instrumental_wav, prefix, score)

    # Rename midi/musicxml to match final prefix, clean up temp instrumental files
    for ext in (".mid", ".musicxml", ".manifest.json"):
        tmp_path = os.path.join(TRACK_DIR, f"{instrumental_prefix}{ext}")
        final_path = os.path.join(TRACK_DIR, f"{prefix}{ext}")
        if os.path.exists(tmp_path):
            os.replace(tmp_path, final_path)
    if os.path.exists(instrumental_wav):
        os.remove(instrumental_wav)

    tag_mp3(out_mp3, score, art_path)

    acoustic = studio.analyze_audio_file(out_wav)
    print(f"  [Acoustics] LUFS: {acoustic.integrated_lufs_estimate:.2f}, "
          f"Dynamic Range: {acoustic.dynamic_range_db:.2f} dB, "
          f"True Peak: {acoustic.true_peak_dbfs:.2f} dBFS, "
          f"Spectral Centroid: {acoustic.spectral_centroid_hz:.1f} Hz, "
          f"Dissonance Index: {acoustic.dissonance_index:.3f}")

    diag = studio.diagnose_audio(out_wav)
    print(f"  [Diagnostics] {diag}")
    print("=== BONUS TRACK 2 COMPILATION COMPLETE ===")


if __name__ == "__main__":
    compile_bonus_track_2()
