"""
CHRONOSIGNATURES (Annex): "The Braid That Doesn't Commute"
Bonus track by Claude Sonnet 5, reinterpreting Track 03 (Noncommutative Horizon) as
a downtempo piece in G harmonic minor, 7/8.

Two waveguide-plucked string voices play the same motif in forward and reversed
chord-tone order, panned apart, never resolving into unison. Uses two engine
instruments unused elsewhere on the album:
- CloudGranularSynth, via the render_note() adapter added to
  harmonia/dsp/synths/granular.py (HARMONIA_WISHLIST.md item 1).
- DigitalWaveguideStringSynth as the lead voice.
"""

import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON, TCOP, COMM

from harmonia.ir.schema import (
    Score, ChordDef, MacroBlock, MasteringConfig, VoicePocketConfig, TrackChannel, SendBusDef, FXDef, NoteEvent
)
from harmonia.ir.parser import ScoreParser
from harmonia.tools.api import HarmoniaStudio

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACK_DIR = os.path.join(REPO_ROOT, "tracks")
ART_DIR = os.path.join(REPO_ROOT, "art")


def build_score() -> Score:
    # G harmonic minor: G A Bb C D Eb F# (43 45 46 48 50 51 54)
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

    # Sparse 7/8 pulse for the climax only (14 eighth-note steps: 3+2+2 feel, same as Track 03)
    rhythm_sparse_7_8 = {
        "kick":  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "snare": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "hat":   [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    }

    timeline = [
        MacroBlock("1_Operator_A", "MAIN", num_bars=8, energy=0.35,
                   has_drums=False, has_bass=False, has_pad=True, has_stabs=False,
                   has_bells=True, has_vocaloid=False, filter_cutoff=650.0,
                   groove_profile="bossa_drift"),
        MacroBlock("2_Operator_B_Reordered", "MAIN", num_bars=8, energy=0.52,
                   has_drums=False, has_bass=False, has_pad=True, has_stabs=False,
                   has_bells=True, has_vocaloid=False, filter_cutoff=800.0,
                   groove_profile="bossa_drift"),
        MacroBlock("3_The_Discrepancy", "MAIN", num_bars=10, energy=0.82,
                   has_drums=True, has_bass=False, has_pad=True, has_stabs=False,
                   has_bells=True, has_vocaloid=True, filter_cutoff=1050.0,
                   groove_profile="bossa_drift", rhythm_patterns=rhythm_sparse_7_8),
        MacroBlock("4_Dissolve", "MAIN", num_bars=8, energy=0.30,
                   has_drums=False, has_bass=False, has_pad=True, has_stabs=False,
                   has_bells=True, has_vocaloid=False, filter_cutoff=550.0,
                   groove_profile="bossa_drift"),
    ]

    quarter_notes_per_bar = 3.5  # 7/8
    total_bars = sum(b.num_bars for b in timeline)

    # Motif: chord-tone degrees within each chord's pad_notes, taken low-to-high
    motif_degrees_fwd = [0, 1, 2, 3]
    motif_degrees_rev = [3, 2, 1, 0]

    def motif_events(degree_order, start_bar, end_bar, pan, base_velocity, instrument_gain=1.0):
        events = []
        for bar in range(start_bar, end_bar):
            chord = chords[bar % len(chords)]
            b_start = bar * quarter_notes_per_bar
            # One note per bar, held for most of the bar, walking the motif degree order
            deg = degree_order[bar % len(degree_order)]
            note = chord.pad_notes[deg % len(chord.pad_notes)]
            events.append(NoteEvent(
                start_beat=b_start,
                duration_beats=quarter_notes_per_bar * 0.92,
                midi_note=note,
                velocity=base_velocity * instrument_gain,
                pan=pan
            ))
        return events

    # String voice A: forward order, present the entire piece (constant identity)
    string_fwd_events = motif_events(motif_degrees_fwd, 0, total_bars, pan=-0.35, base_velocity=0.55)
    # String voice B: reversed order, only enters once "Operator B" is applied (bar 8+)
    string_rev_events = motif_events(motif_degrees_rev, 8, total_bars, pan=0.40, base_velocity=0.50)

    string_fwd_channel = TrackChannel(
        id="string_voice_fwd",
        instrument_id="waveguide",
        events=string_fwd_events,
        fx_chain=[
            FXDef(plugin_type="filter", params={"cutoff_hz": 5200.0, "mode": "lowpass"}),
        ],
        sends={"chamber_verb": 0.42},
        volume_db=-2.0,
        pan=-0.35
    )
    string_rev_channel = TrackChannel(
        id="string_voice_rev",
        instrument_id="waveguide",
        events=string_rev_events,
        fx_chain=[
            FXDef(plugin_type="filter", params={"cutoff_hz": 4600.0, "mode": "lowpass"}),
        ],
        sends={"chamber_verb": 0.48},
        volume_db=-2.8,
        pan=0.40
    )

    # Granular cloud voice: long evolving textures, one per 2 bars, root + fifth
    granular_events = []
    for bar in range(0, total_bars, 2):
        chord = chords[bar % len(chords)]
        b_start = bar * quarter_notes_per_bar
        section_energy = 0.4 if bar < 8 else (0.55 if bar < 16 else (0.9 if bar < 26 else 0.45))
        for note in [chord.bass_midi + 12, chord.pad_notes[-1]]:
            granular_events.append(NoteEvent(
                start_beat=b_start,
                duration_beats=quarter_notes_per_bar * 2.1,
                midi_note=note,
                velocity=0.30 * section_energy,
                pan=0.0
            ))
    granular_channel = TrackChannel(
        id="granular_atmosphere",
        instrument_id="granular",
        events=granular_events,
        fx_chain=[
            FXDef(plugin_type="dimension", params={"width": 1.9, "hp_side_hz": 220.0}),
        ],
        sends={"chamber_verb": 0.60},
        volume_db=-4.0,
        pan=0.0
    )

    # Acid bass undertow: slow root pulses, enters with "Operator B", drives the climax
    acid_events = []
    for bar in range(8, total_bars):
        chord = chords[bar % len(chords)]
        b_start = bar * quarter_notes_per_bar
        section_energy = 0.6 if bar < 16 else (1.0 if bar < 26 else 0.5)
        acid_events.append(NoteEvent(
            start_beat=b_start,
            duration_beats=quarter_notes_per_bar * 0.85,
            midi_note=chord.bass_midi - 12,
            velocity=0.75 * section_energy,
            pan=0.0
        ))
    acid_channel = TrackChannel(
        id="acid_undertow",
        instrument_id="acid_bass",
        events=acid_events,
        fx_chain=[
            FXDef(plugin_type="filter", params={"cutoff_hz": 380.0, "resonance": 1.6, "mode": "lowpass"}),
            FXDef(plugin_type="distortion", params={"drive": 1.3, "mode": "diode", "tone": 0.45}, mix=0.35),
        ],
        sends={"undertow_room": 0.30},
        volume_db=-1.5,
        pan=0.0
    )

    send_busses = {
        "chamber_verb": SendBusDef(
            id="chamber_verb",
            fx_chain=[
                FXDef(plugin_type="reverb", params={"decay_time_s": 4.6, "damp_hz": 3800.0}, mix=1.0),
                FXDef(plugin_type="dimension", params={"width": 1.7, "hp_side_hz": 200.0}),
            ],
            volume_db=-4.5
        ),
        "undertow_room": SendBusDef(
            id="undertow_room",
            fx_chain=[
                FXDef(plugin_type="reverb", params={"decay_time_s": 1.6}, mix=0.6),
            ],
            volume_db=-6.0
        )
    }

    master_bus_fx = [
        FXDef(plugin_type="dimension", params={"width": 1.30, "hp_side_hz": 190.0}),
        FXDef(plugin_type="distortion", params={"drive": 1.05, "mode": "tape", "tone": 0.80}, mix=0.10),
    ]

    return Score(
        title="09 The Braid That Doesn't Commute",
        schema_version="2.3",
        seed=909909,
        bpm=63.0,
        meter_numerator=7,
        meter_denominator=8,
        key_root="G",
        scale_type="harmonic_minor",
        groove_profile="bossa_drift",
        swing_ratio=0.52,
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[string_fwd_channel, string_rev_channel, granular_channel, acid_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(
            target_lufs=-18.0,
            peak_ceiling_db=-1.5,
            tape_warmth_enabled=True,
            fade_in_s=1.5,
            fade_out_s=5.0,
            voice_pocket=VoicePocketConfig(enabled=True, center_freq_hz=2400.0, gain_db=-3.2)
        ),
        metadata={
            "track_number": 9,
            "bonus_track": True,
            "based_on": "03 Noncommutative Horizon",
            "author": "Claude (Sonnet 5) -- creative side-experiment, not part of Gemini's main 8-track run",
            "concept": (
                "Two symmetry operators applied in either order land somewhere different. "
                "The same four-note motif is played by two waveguide-plucked string voices, "
                "one forward, one reversed, panned apart, never resolving into unison -- "
                "the discrepancy between orders made audible. G harmonic minor's raised 7th, "
                "and a borrowed natural 9 in the final chord's sharp-5, are the 'wrong notes' "
                "that keep the symmetry from ever quite closing."
            )
        }
    )


def tag_mp3(mp3_path: str, score: Score, art_path: str):
    if not os.path.exists(mp3_path):
        return
    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass

    audio.tags.add(TIT2(encoding=3, text="The Braid That Doesn't Commute"))
    audio.tags.add(TPE1(encoding=3, text="Harmonia Engine · Claude"))
    audio.tags.add(TPE2(encoding=3, text="Harmonia Engine · Claude"))
    audio.tags.add(TALB(encoding=3, text="Chronosignatures (Annex)"))
    audio.tags.add(TRCK(encoding=3, text="9"))
    audio.tags.add(TDRC(encoding=3, text="2026"))
    audio.tags.add(TCON(encoding=3, text="Ambient / Downtempo Glitch"))
    audio.tags.add(TCOP(encoding=3, text="© 2026 Harmonia Engine"))
    audio.tags.add(COMM(encoding=3, lang="eng", desc="Description", text=score.metadata.get("concept", "")))

    if os.path.exists(art_path):
        with open(art_path, "rb") as img_f:
            audio.tags.add(APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,
                desc="Cover",
                data=img_f.read()
            ))
    audio.save(v2_version=3)
    print(f"  [ID3 Tagged] {mp3_path} with art: {art_path}")


def compile_bonus_track():
    score = build_score()
    art_path = os.path.join(ART_DIR, "09_the_braid_that_doesnt_commute.jpg")

    studio = HarmoniaStudio()
    print("=== COMPILING BONUS TRACK: 'The Braid That Doesn't Commute' ===")
    ScoreParser.validate(score)

    prefix = "09_the_braid_that_doesnt_commute"
    wav_path = os.path.join(TRACK_DIR, f"{prefix}.wav")
    json_path = os.path.join(TRACK_DIR, f"{prefix}.json")
    ScoreParser.save_to_file(score, json_path)
    print(f"  Saved Score IR: {json_path}")

    res = studio.compile_score(
        score,
        output_path=wav_path,
        export_mp3=True,
        export_stems=False,
        export_midi=True,
        export_musicxml=True
    )
    print(f"  Rendered WAV: {wav_path}")
    print(f"  Exported MP3: {res.get('mp3')}")
    print(f"  Score Fingerprint: {res['score_fingerprint']}")

    if res.get("mp3"):
        tag_mp3(res["mp3"], score, art_path)

    acoustic = studio.analyze_audio_file(wav_path)
    print(f"  [Acoustics] LUFS: {acoustic.integrated_lufs_estimate:.2f}, "
          f"Dynamic Range: {acoustic.dynamic_range_db:.2f} dB, "
          f"True Peak: {acoustic.true_peak_dbfs:.2f} dBFS, "
          f"Spectral Centroid: {acoustic.spectral_centroid_hz:.1f} Hz, "
          f"Rolloff: {acoustic.spectral_rolloff_hz:.1f} Hz, "
          f"Dissonance Index: {acoustic.dissonance_index:.3f}")

    diag = studio.diagnose_audio(wav_path)
    print(f"  [Diagnostics] {diag}")

    print("=== BONUS TRACK COMPILATION COMPLETE ===")


if __name__ == "__main__":
    compile_bonus_track()
