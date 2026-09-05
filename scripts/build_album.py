"""
CHRONOSIGNATURES: Noncommutative Geodesics of an Artificial Mind
Master Album Builder, Procedural Compiler, and Acoustic/Symbolic Analysis Pipeline.
Harmonia Engine v2.3 Modular Workstation Architecture.
"""

import os
import json
import time
import shutil
import numpy as np
import scipy.io.wavfile as wavfile
from mutagen.mp3 import MP3
import re
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON, TCOP, COMM

TRACK_GENRES = {
    1: "Ambient",
    2: "UK Garage",
    3: "Progressive Electronic",
    4: "Lo-Fi / Neo Soul",
    5: "Electro Swing",
    6: "Cinematic Electronic",
}

from harmonia.ir.schema import (
    Score, ChordDef, MacroBlock, MasteringConfig, VoicePocketConfig, AutomationCurve, CurvePoint,
    TrackChannel, SendBusDef, FXDef, NoteEvent
)
from harmonia.ir.parser import ScoreParser
from harmonia.tools.api import HarmoniaStudio
from harmonia.mixer.analysis import AudioAcousticAnalyzer
from harmonia.theory.metrics import analyze_score
from harmonia.theory.mozart import probe_progression
from harmonia.theory.signature import chord_path, musical_signature_report
from harmonia.theory.information import universal_information_dynamics
from harmonia.generative.determinism import content_fingerprint
from harmonia.dsp.synths.formant_vocal import FormantVocaloidSynth
from harmonia.dsp.drums.drum_engine import HarmoniaDrumEngine
from harmonia.dsp.primitives import StudioConvolutionReverb, apply_tpdf_dither, add_to_track
from harmonia.mixer.mastering import BroadcastMasteringEngine
from harmonia.mixer.voice_pocket import VoicePocketProcessor
import subprocess
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALBUM_DIR = os.path.join(REPO_ROOT, "tracks")
ART_DIR = os.path.join(REPO_ROOT, "art")
os.makedirs(ALBUM_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)


def build_track_1() -> Score:
    """
    Track 1: Zero Temperature Limit (F Lydian, 68 BPM, Ambient / Floating Glass)
    Acoustic DNA:
    - Pristine zero-entropy ground state in cold Lydian space.
    - Ethereal shimmer plate reverb with Haas Mid-Side dimension expansion.
    - Subtle 0.75-beat ping-pong echoes and master bus analog tape warmth.
    """
    chords = [
        ChordDef("Fmaj9#11", bass_midi=41, pad_notes=[53, 57, 60, 64, 67, 71], stab_notes=[60, 64, 67], bell_notes=[64, 67, 71, 72, 76], vocal_notes=[72, 76]),
        ChordDef("G9sus4", bass_midi=43, pad_notes=[55, 60, 62, 65, 69], stab_notes=[60, 62, 65], bell_notes=[62, 65, 69, 74], vocal_notes=[74, 72]),
        ChordDef("Am11", bass_midi=45, pad_notes=[57, 60, 64, 67, 71, 74], stab_notes=[60, 64, 67], bell_notes=[64, 67, 71, 76], vocal_notes=[76, 74]),
        ChordDef("Em9", bass_midi=40, pad_notes=[52, 55, 59, 62, 66], stab_notes=[55, 59, 62], bell_notes=[59, 62, 66, 71], vocal_notes=[71, 67]),
    ]
    timeline = [
        MacroBlock("1_Ground_State", "MAIN", num_bars=6, energy=0.55, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=650.0, groove_profile="bossa_drift"),
        MacroBlock("2_Permutation_Symmetry", "MAIN", num_bars=6, energy=0.72, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=900.0, groove_profile="bossa_drift", rhythm_patterns={
            "kick": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            "snare": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "hat": [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
        }),
        MacroBlock("3_Condensate_Peak", "MAIN", num_bars=6, energy=0.88, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=True, filter_cutoff=1250.0, groove_profile="bossa_drift", rhythm_patterns={
            "kick": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "hat": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        }),
        MacroBlock("4_Zero_Entropy_Return", "MAIN", num_bars=6, energy=0.45, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=550.0, groove_profile="bossa_drift"),
    ]
    total_bars_t1 = sum(b.num_bars for b in timeline)

    # Removing the block stabs opens space rather than needing to be filled -- that's
    # the actual ambient move. Granular "Cryo-Mist" adds one barely-there texture: a
    # long, sparse, high-frequency haze sitting well under the pad/bell bed, not a
    # foreground voice.
    mist_events = []
    for bar in range(0, total_bars_t1, 6):
        chord = chords[bar % len(chords)]
        b_start = bar * 4.0
        mist_events.append(NoteEvent(
            start_beat=b_start, duration_beats=22.0,
            midi_note=chord.pad_notes[-1] + 12, velocity=0.18, pan=0.0
        ))
    mist_channel = TrackChannel(
        id="granular_cryo_mist", instrument_id="granular", events=mist_events,
        fx_chain=[FXDef(plugin_type="dimension", params={"width": 1.8, "hp_side_hz": 250.0})],
        sends={"shimmer_reverb": 0.70}, volume_db=-7.5, pan=0.0
    )

    send_busses = {
        "shimmer_reverb": SendBusDef(
            id="shimmer_reverb",
            fx_chain=[
                FXDef(plugin_type="reverb", params={"decay_time_s": 3.0}, mix=1.0),
                FXDef(plugin_type="dimension", params={"width": 1.6, "hp_side_hz": 200.0}),
            ],
            volume_db=-3.5
        ),
        "ambient_delay": SendBusDef(
            id="ambient_delay",
            fx_chain=[
                FXDef(plugin_type="delay", params={"delay_time_s": 0.662, "feedback": 0.35, "damp_hz": 3600.0}, mix=1.0),
            ],
            volume_db=-4.0
        )
    }
    master_bus_fx = [
        FXDef(plugin_type="dimension", params={"width": 1.35, "hp_side_hz": 180.0}),
        FXDef(plugin_type="distortion", params={"drive": 1.10, "mode": "tape", "tone": 0.85}, mix=0.15),
    ]
    return Score(
        title="01 Zero Temperature Limit",
        schema_version="2.3",
        seed=101,
        bpm=68.0,
        meter_numerator=4,
        meter_denominator=4,
        key_root="F",
        scale_type="lydian",
        groove_profile="bossa_drift",
        swing_ratio=0.53,
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[mist_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(target_lufs=-17.2, peak_ceiling_db=-0.8, voice_pocket=VoicePocketConfig(enabled=True, center_freq_hz=2600.0, gain_db=-3.0)),
        metadata={"track_number": 1, "concept": "Zero-entropy ground state of an artificial observer in cold Lydian space."}
    )


def build_track_2() -> Score:
    """
    Track 2: Circulation on the Simplex (D Dorian, 128 BPM, UK Garage / 2-Step)
    Acoustic DNA:
    - Orthogonal Hodge cycle circulation over D Dorian discrete transition currents.
    - Punchy 2-step syncopation with snappy TR-909 multi-pulse claps.
    - Chord stabs with stereo chorus and transient punch, bus glue compression.
    """
    chords = [
        ChordDef("Dm9", bass_midi=38, pad_notes=[50, 53, 57, 60, 64], stab_notes=[57, 60, 64], bell_notes=[65, 69, 72, 76], vocal_notes=[72, 69]),
        ChordDef("G13", bass_midi=43, pad_notes=[55, 59, 62, 65, 69, 71], stab_notes=[59, 64, 69], bell_notes=[67, 71, 74, 77], vocal_notes=[74, 71]),
        ChordDef("Cmaj9", bass_midi=36, pad_notes=[48, 52, 55, 59, 62], stab_notes=[55, 59, 62], bell_notes=[64, 67, 71, 74], vocal_notes=[71, 67]),
        ChordDef("Em7b5", bass_midi=40, pad_notes=[52, 55, 58, 62], stab_notes=[55, 58, 62], bell_notes=[62, 65, 70, 74], vocal_notes=[70, 65]),
    ]
    rhythm_ukg = {
        "kick": [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "hat": [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
    }
    timeline = [
        MacroBlock("1_Current_Initialization", "MAIN", num_bars=8, energy=0.70, has_drums=False, has_bass=False, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=800.0, groove_profile="ukg_syncopate"),
        MacroBlock("2_Cyclic_Decomposition", "MAIN", num_bars=12, energy=0.92, has_drums=True, has_bass=False, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=1100.0, groove_profile="ukg_syncopate", rhythm_patterns=rhythm_ukg),
        MacroBlock("3_Hodge_Singularity", "MAIN", num_bars=12, energy=0.98, has_drums=True, has_bass=False, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=True, filter_cutoff=1350.0, groove_profile="ukg_syncopate", rhythm_patterns=rhythm_ukg),
        MacroBlock("4_Boundary_Transport", "MAIN", num_bars=8, energy=0.60, has_drums=False, has_bass=False, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=700.0, groove_profile="ukg_syncopate"),
    ]
    # UKG Syncopated Bass: replaces the static root-note drone with a bouncy,
    # octave-jumping acid line. Density and shape shift with each block instead of
    # repeating one fixed pattern for all 40 bars -- sparse in the intro, full through
    # the build, an extra ghost note at the peak, thinning back down for the outro.
    bass_events = []
    bar_cursor = 0
    for block in timeline:
        for i in range(block.num_bars):
            bar = bar_cursor + i
            chord = chords[bar % len(chords)]
            b_start = bar * 4.0
            root = chord.bass_midi
            if block.name == "1_Current_Initialization":
                bass_events.extend([
                    NoteEvent(start_beat=b_start + 0.75, duration_beats=0.4, midi_note=root, velocity=0.70),
                    NoteEvent(start_beat=b_start + 2.25, duration_beats=0.4, midi_note=root, velocity=0.65),
                ])
            elif block.name == "3_Hodge_Singularity":
                jump = 19 if (bar % 2 == 0) else 12
                bass_events.extend([
                    NoteEvent(start_beat=b_start + 0.75, duration_beats=0.3, midi_note=root, velocity=0.88),
                    NoteEvent(start_beat=b_start + 1.5, duration_beats=0.2, midi_note=root + jump, velocity=0.78),
                    NoteEvent(start_beat=b_start + 2.0, duration_beats=0.2, midi_note=root + 7, velocity=0.70),
                    NoteEvent(start_beat=b_start + 2.25, duration_beats=0.3, midi_note=root, velocity=0.85),
                    NoteEvent(start_beat=b_start + 3.5, duration_beats=0.4, midi_note=root + jump, velocity=0.85),
                ])
            elif block.name == "4_Boundary_Transport":
                bass_events.append(
                    NoteEvent(start_beat=b_start + 0.75, duration_beats=0.5, midi_note=root, velocity=0.60 - 0.02 * i)
                )
            else:  # 2_Cyclic_Decomposition -- the original full pattern
                bass_events.extend([
                    NoteEvent(start_beat=b_start + 0.75, duration_beats=0.35, midi_note=root, velocity=0.85),
                    NoteEvent(start_beat=b_start + 1.5, duration_beats=0.25, midi_note=root + 12, velocity=0.75),
                    NoteEvent(start_beat=b_start + 2.25, duration_beats=0.35, midi_note=root, velocity=0.82),
                    NoteEvent(start_beat=b_start + 3.5, duration_beats=0.4, midi_note=root + 7, velocity=0.80),
                ])
        bar_cursor += block.num_bars
    ukg_bass_channel = TrackChannel(
        id="ukg_syncopated_bass", instrument_id="acid_bass", events=bass_events,
        fx_chain=[
            FXDef(plugin_type="filter", params={"cutoff_hz": 900.0, "resonance": 1.8, "mode": "lowpass", "envelope_mod": 0.5}),
            FXDef(plugin_type="distortion", params={"drive": 1.4, "mode": "diode", "tone": 0.6}, mix=0.4),
        ],
        sends={"dub_space": 0.20}, volume_db=0.0, pan=0.0
    )

    send_busses = {
        "dub_space": SendBusDef(
            id="dub_space",
            fx_chain=[
                FXDef(plugin_type="delay", params={"delay_time_s": 0.352, "feedback": 0.32, "damp_hz": 4000.0}),
                FXDef(plugin_type="reverb", params={"decay_time_s": 1.8}, mix=0.5),
            ],
            volume_db=-4.5
        )
    }
    master_bus_fx = [
        FXDef(plugin_type="transient", params={"attack_db": 1.8, "sustain_db": -0.6}),
        FXDef(plugin_type="distortion", params={"drive": 1.15, "mode": "tape", "tone": 0.75}, mix=0.20),
    ]
    return Score(
        title="02 Circulation on the Simplex",
        schema_version="2.3",
        seed=202,
        bpm=128.0,
        meter_numerator=4,
        meter_denominator=4,
        key_root="D",
        scale_type="dorian",
        groove_profile="ukg_syncopate",
        swing_ratio=0.59,
        drum_kit="ukg",
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[ukg_bass_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(target_lufs=-15.0, peak_ceiling_db=-0.8, sidechain_duck_db=4.2),
        metadata={"track_number": 2, "concept": "Orthogonal Hodge cycle circulation over D Dorian discrete transition currents."}
    )


def build_track_3() -> Score:
    """
    Track 3: Noncommutative Horizon (G Minor, 94 BPM, 7/8 Odd-Meter Progressive Glitch)
    Acoustic DNA:
    - Asymmetric 7/8 temporal metric probing non-Abelian Lie brackets and path signatures.
    - Polyrhythmic 7/8 fractional delay line and spatial dimension expansion.
    - Clean odd-meter Euclidean rimshot backbeats on subdivisions 3 and 8.
    """
    chords = [
        ChordDef("Gm9", bass_midi=43, pad_notes=[55, 58, 62, 65, 69], stab_notes=[58, 62, 65], bell_notes=[65, 69, 72, 77], vocal_notes=[72, 69]),
        ChordDef("Ebmaj7#11", bass_midi=39, pad_notes=[51, 55, 58, 62, 65, 69], stab_notes=[55, 58, 62], bell_notes=[63, 67, 70, 75], vocal_notes=[75, 70]),
        ChordDef("F9sus4", bass_midi=41, pad_notes=[53, 58, 60, 63, 67], stab_notes=[58, 60, 63], bell_notes=[65, 68, 72, 75], vocal_notes=[72, 68]),
        ChordDef("Dm7b5", bass_midi=38, pad_notes=[50, 53, 56, 60], stab_notes=[53, 56, 60], bell_notes=[62, 65, 68, 74], vocal_notes=[68, 65]),
    ]
    # 7/8 meter = 14 sixteenth-note subdivisions (3+2+2 rhythm)
    rhythm_7_8 = {
        "kick":  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        "snare": [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "hat":   [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    }
    climax_filter_curve = AutomationCurve(
        base_value=1050.0,
        points=[
            CurvePoint(0.0, 750.0, "smooth"),
            CurvePoint(0.43, 1450.0, "smooth"),
            CurvePoint(0.71, 900.0, "smooth"),
            CurvePoint(1.0, 1280.0, "smooth"),
        ]
    )
    timeline = [
        MacroBlock("1_Event_Boundary", "MAIN", num_bars=8, energy=0.65, has_drums=False, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=750.0, groove_profile="straight"),
        MacroBlock("2_Lie_Bracket_Distortion", "MAIN", num_bars=8, energy=0.86, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=1050.0, groove_profile="straight", filter_curve=climax_filter_curve, rhythm_patterns=rhythm_7_8),
        MacroBlock("3_Noncommutative_Singularity", "MAIN", num_bars=8, energy=0.95, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=True, filter_cutoff=1280.0, groove_profile="straight", filter_curve=climax_filter_curve, rhythm_patterns=rhythm_7_8),
        MacroBlock("4_Radiation_Afterglow", "MAIN", num_bars=8, energy=0.50, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=600.0, groove_profile="straight"),
    ]

    # Dual Polyrhythmic Counterpoint: two voices traverse the 7/8 bar in opposite chord-
    # tone orders through the two busiest blocks (bars 8-23), embodying the noncommutative
    # premise structurally: same material, different order, different result.
    qnpb_78 = 3.5
    degrees_fwd = [0, 1, 2, 3]
    degrees_rev = [3, 2, 1, 0]
    counterpoint_fwd, counterpoint_rev = [], []
    for bar in range(8, 24):
        chord = chords[bar % len(chords)]
        b_start = bar * qnpb_78
        note_fwd = chord.pad_notes[degrees_fwd[bar % 4] % len(chord.pad_notes)]
        note_rev = chord.pad_notes[degrees_rev[bar % 4] % len(chord.pad_notes)]
        counterpoint_fwd.append(NoteEvent(start_beat=b_start, duration_beats=qnpb_78 * 0.85, midi_note=note_fwd, velocity=0.55, pan=-0.3))
        counterpoint_rev.append(NoteEvent(start_beat=b_start, duration_beats=qnpb_78 * 0.85, midi_note=note_rev + 12, velocity=0.5, pan=0.3))

    counterpoint_fwd_channel = TrackChannel(
        id="counterpoint_waveguide", instrument_id="waveguide", events=counterpoint_fwd,
        fx_chain=[FXDef(plugin_type="filter", params={"cutoff_hz": 5000.0, "mode": "lowpass"})],
        sends={"polyrhythm_delay": 0.35}, volume_db=-2.0, pan=-0.3
    )
    counterpoint_rev_channel = TrackChannel(
        id="counterpoint_tape_synth", instrument_id="supersaw", events=counterpoint_rev,
        fx_chain=[
            FXDef(plugin_type="distortion", params={"drive": 1.6, "mode": "tape", "tone": 0.55}, mix=0.5),
            FXDef(plugin_type="filter", params={"cutoff_hz": 3200.0, "mode": "lowpass"}),
        ],
        sends={"polyrhythm_delay": 0.3}, volume_db=-4.0, pan=0.3
    )

    send_busses = {
        "polyrhythm_delay": SendBusDef(
            id="polyrhythm_delay",
            fx_chain=[
                FXDef(plugin_type="delay", params={"delay_time_s": 0.319, "feedback": 0.35, "damp_hz": 3200.0}),
            ],
            volume_db=-4.0
        )
    }
    master_bus_fx = [
        FXDef(plugin_type="dimension", params={"width": 1.25, "hp_side_hz": 220.0}),
        FXDef(plugin_type="distortion", params={"drive": 1.20, "mode": "tape", "tone": 0.70}, mix=0.22),
    ]
    return Score(
        title="03 Noncommutative Horizon",
        schema_version="2.3",
        seed=303,
        bpm=94.0,
        meter_numerator=7,
        meter_denominator=8,
        key_root="G",
        scale_type="natural_minor",
        groove_profile="straight",
        swing_ratio=0.50,
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[counterpoint_fwd_channel, counterpoint_rev_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(target_lufs=-15.4, peak_ceiling_db=-0.8, sidechain_duck_db=3.8),
        metadata={"track_number": 3, "concept": "Asymmetric 7/8 temporal metric probing non-Abelian path signature components."}
    )


def build_track_4() -> Score:
    """
    Track 4: The Aitchison Drift (Bb Major, 76 BPM, J Dilla Drag / Lo-Fi Soul)
    Acoustic DNA:
    - Mellow unquantized Aitchison simplex drift with analog tape compression, Rhodes FM keys, and MPC drag.
    - Deep 808 sub kick and soft woody rimshots.
    - Warm plate reverb with rolled-off highs and gentle compression swell.
    """
    chords = [
        ChordDef("Bbmaj9", bass_midi=46, pad_notes=[58, 62, 65, 69, 72], stab_notes=[62, 65, 69, 72], bell_notes=[70, 74, 77, 81], vocal_notes=[77, 74]),
        ChordDef("Cm9", bass_midi=48, pad_notes=[60, 63, 67, 70, 74], stab_notes=[63, 67, 70, 74], bell_notes=[72, 75, 79, 82], vocal_notes=[79, 75]),
        ChordDef("Dm7", bass_midi=50, pad_notes=[62, 65, 69, 72], stab_notes=[65, 69, 72, 76], bell_notes=[74, 77, 81, 84], vocal_notes=[81, 77]),
        ChordDef("Ebmaj7#11", bass_midi=51, pad_notes=[63, 67, 70, 74, 77, 81], stab_notes=[67, 70, 74, 77], bell_notes=[75, 79, 82, 86], vocal_notes=[82, 79]),
    ]
    rhythm_dilla = {
        "kick":  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "hat":   [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    }
    timeline = [
        MacroBlock("1_Simplicial_Warmth", "MAIN", num_bars=6, energy=0.68, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=False, filter_cutoff=750.0, groove_profile="j_dilla_drag"),
        MacroBlock("2_Unquantized_Flow", "MAIN", num_bars=8, energy=0.84, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=950.0, groove_profile="j_dilla_drag", rhythm_patterns=rhythm_dilla),
        MacroBlock("3_Aitchison_Subspace", "MAIN", num_bars=8, energy=0.90, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=True, filter_cutoff=1100.0, groove_profile="j_dilla_drag", rhythm_patterns=rhythm_dilla),
        MacroBlock("4_Tape_Fadeout", "MAIN", num_bars=6, energy=0.55, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=650.0, groove_profile="j_dilla_drag"),
    ]
    total_bars_t4 = sum(b.num_bars for b in timeline)

    # Humanized Rhodes voicings: staggered strum delays (~25-55ms) and per-note velocity
    # weighting replace the block chord stabs for a less quantized, more played feel.
    rng4 = np.random.default_rng(404)
    strum_events = []
    for bar in range(total_bars_t4):
        chord = chords[bar % len(chords)]
        b_start = bar * 4.0
        for i, note in enumerate(chord.stab_notes):
            stagger_beats = (0.02 + i * 0.012) * rng4.uniform(0.85, 1.15)
            vel = float(rng4.uniform(0.55, 0.78))
            strum_events.append(NoteEvent(start_beat=b_start + stagger_beats, duration_beats=1.6, midi_note=note, velocity=vel))
    humanized_keys_channel = TrackChannel(
        id="humanized_rhodes", instrument_id="fm_keys", events=strum_events,
        fx_chain=[FXDef(plugin_type="chorus", params={"rate_hz": 0.5, "depth_ms": 2.0}, mix=0.25)],
        sends={"warm_plate": 0.30}, volume_db=-3.0, pan=0.0
    )

    send_busses = {
        "warm_plate": SendBusDef(
            id="warm_plate",
            fx_chain=[
                FXDef(plugin_type="reverb", params={"decay_time_s": 2.2}, mix=1.0),
                FXDef(plugin_type="filter", params={"cutoff_hz": 3400.0, "mode": "lowpass"}),
            ],
            volume_db=-4.0
        )
    }
    master_bus_fx = [
        FXDef(plugin_type="distortion", params={"drive": 1.35, "mode": "tape", "tone": 0.65}, mix=0.28),
        FXDef(plugin_type="transient", params={"attack_db": -0.5, "sustain_db": 0.8}),
    ]
    return Score(
        title="04 The Aitchison Drift",
        schema_version="2.3",
        seed=404,
        bpm=76.0,
        meter_numerator=4,
        meter_denominator=4,
        key_root="Bb",
        scale_type="major",
        groove_profile="j_dilla_drag",
        swing_ratio=0.62,
        drum_kit="808_trap",
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[humanized_keys_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(target_lufs=-15.8, peak_ceiling_db=-0.8, tape_warmth_enabled=True, sidechain_duck_db=3.8),
        metadata={"track_number": 4, "concept": "Mellow unquantized Aitchison simplex drift with analog tape compression and MPC swing."}
    )


def build_track_5() -> Score:
    """
    Track 5: Cumulant Cascade (A Dorian, 114 BPM, Electro-Swing / Neo-Bop)
    Acoustic DNA:
    - Fast-paced Taylor cumulant series expansion driven by heavy MPC swing (0.66).
    - Punchy brass stabs with transient bite, bouncy electro-swing kit with crisp claps.
    - Subtle room reverb and analog tape master warmth.
    """
    chords = [
        ChordDef("Am9", bass_midi=45, pad_notes=[57, 60, 64, 67, 71], stab_notes=[60, 64, 67, 71], bell_notes=[69, 72, 76, 79], vocal_notes=[76, 72]),
        ChordDef("D9", bass_midi=50, pad_notes=[57, 62, 66, 69, 72], stab_notes=[62, 66, 69], bell_notes=[66, 69, 74, 78], vocal_notes=[74, 69]),
        ChordDef("Fmaj7", bass_midi=41, pad_notes=[53, 57, 60, 64, 69], stab_notes=[57, 60, 64], bell_notes=[65, 69, 72, 76], vocal_notes=[72, 65]),
        ChordDef("E7#9", bass_midi=40, pad_notes=[52, 56, 59, 62, 67], stab_notes=[56, 59, 62, 67], bell_notes=[64, 68, 71, 75], vocal_notes=[75, 68]),
    ]
    rhythm_swing = {
        "kick":  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "hat":   [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    }
    timeline = [
        MacroBlock("1_Vintage_Axiom", "MAIN", num_bars=6, energy=0.72, has_drums=False, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=850.0, groove_profile="mpc_swing_66"),
        MacroBlock("2_Higher_Moment_Burst", "MAIN", num_bars=10, energy=0.90, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=1150.0, groove_profile="mpc_swing_66", rhythm_patterns=rhythm_swing),
        MacroBlock("3a_Breakdown", "MAIN", num_bars=2, energy=0.45, has_drums=False, has_bass=False, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=True, filter_cutoff=700.0, groove_profile="mpc_swing_66"),
        MacroBlock("3b_Cumulant_Convergence", "MAIN", num_bars=8, energy=0.98, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=True, filter_cutoff=1300.0, groove_profile="mpc_swing_66", rhythm_patterns=rhythm_swing),
        MacroBlock("4_Resolution_Coda", "MAIN", num_bars=6, energy=0.58, has_drums=False, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=750.0, groove_profile="mpc_swing_66"),
    ]

    # SuperSaw Brass Reinforcement: 7-voice detuned layer under the Gypsy stabs during
    # the two busiest sections (skips the 2-bar breakdown).
    brass_events = []
    for bar_range in [(6, 16), (18, 26)]:
        for bar in range(*bar_range):
            chord = chords[bar % len(chords)]
            b_start = bar * 4.0
            for note in chord.stab_notes:
                brass_events.append(NoteEvent(start_beat=b_start, duration_beats=1.3, midi_note=note + 12, velocity=0.6))
    brass_channel = TrackChannel(
        id="supersaw_brass_reinforcement", instrument_id="supersaw", events=brass_events,
        fx_chain=[
            FXDef(plugin_type="dimension", params={"width": 1.7, "hp_side_hz": 230.0}),
            FXDef(plugin_type="filter", params={"cutoff_hz": 4200.0, "mode": "lowpass"}),
        ],
        sends={"swing_room": 0.25}, volume_db=-4.5, pan=0.0
    )

    # Structural transitions: opening sub-impact, riser into the burst, downlifter into
    # the breakdown, riser back out into the peak.
    transition_events = [
        NoteEvent(start_beat=0.0, duration_beats=2.0, midi_note=30, velocity=0.85),
        NoteEvent(start_beat=20.0, duration_beats=4.0, midi_note=60, velocity=0.82),
        NoteEvent(start_beat=64.0, duration_beats=2.0, midi_note=36, velocity=0.80),
        NoteEvent(start_beat=68.0, duration_beats=4.0, midi_note=60, velocity=0.95),
    ]
    transitions_channel = TrackChannel(
        id="cumulant_transitions", instrument_id="transitions", events=transition_events,
        fx_chain=[FXDef(plugin_type="filter", params={"cutoff_hz": 6000.0, "mode": "lowpass"})],
        sends={"swing_room": 0.30}, volume_db=-1.5, pan=0.0
    )

    send_busses = {
        "swing_room": SendBusDef(
            id="swing_room",
            fx_chain=[
                FXDef(plugin_type="reverb", params={"decay_time_s": 1.4}, mix=1.0),
            ],
            volume_db=-5.0
        )
    }
    master_bus_fx = [
        FXDef(plugin_type="transient", params={"attack_db": 1.4, "sustain_db": -0.6}),
        FXDef(plugin_type="distortion", params={"drive": 1.20, "mode": "tape", "tone": 0.80}, mix=0.20),
    ]
    return Score(
        title="05 Cumulant Cascade",
        schema_version="2.3",
        seed=505,
        bpm=114.0,
        meter_numerator=4,
        meter_denominator=4,
        key_root="A",
        scale_type="dorian",
        groove_profile="mpc_swing_66",
        swing_ratio=0.66,
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[brass_channel, transitions_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(target_lufs=-15.0, peak_ceiling_db=-0.8, sidechain_duck_db=3.5),
        metadata={"track_number": 5, "concept": "Fast-paced Taylor cumulant series expansion driven by heavy MPC swing."}
    )


def build_track_6() -> Score:
    """
    Track 6: The Gauge-Corrected Heart (Db Major, 84 BPM, Climactic UKG / Golden Ratio Arc)
    Acoustic DNA:
    - Gauge-corrected Hamiltonian action E° with macroscopic golden-ratio emotional climax.
    - SuperSaw choir pad reinforcement at phi = 0.618 filter automation peak.
    - Vast cathedral convolution reverb and cinematic dimension widening.
    """
    chords = [
        ChordDef("Dbmaj9", bass_midi=37, pad_notes=[49, 53, 56, 60, 63, 68], stab_notes=[56, 60, 63], bell_notes=[65, 68, 72, 75], vocal_notes=[72, 68]),
        ChordDef("Bbm11", bass_midi=46, pad_notes=[58, 61, 65, 68, 72, 75], stab_notes=[61, 65, 68], bell_notes=[68, 72, 75, 80], vocal_notes=[75, 72]),
        ChordDef("Gbmaj9#11", bass_midi=42, pad_notes=[54, 58, 61, 65, 68, 72], stab_notes=[58, 61, 65], bell_notes=[66, 70, 73, 78], vocal_notes=[73, 70]),
        ChordDef("Ab9sus4", bass_midi=44, pad_notes=[56, 61, 63, 66, 70], stab_notes=[61, 63, 66], bell_notes=[68, 71, 75, 78], vocal_notes=[75, 71]),
    ]
    rhythm_climax = {
        "kick":  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "hat":   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    }
    climax_curve = AutomationCurve(
        base_value=1200.0,
        points=[
            CurvePoint(0.0, 1000.0, "smooth"),
            CurvePoint(0.618, 1600.0, "smooth"),
            CurvePoint(1.0, 1100.0, "smooth"),
        ]
    )
    timeline = [
        MacroBlock("1_Awakening_Potential", "MAIN", num_bars=8, energy=0.65, has_drums=False, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=750.0, groove_profile="ukg_syncopate"),
        MacroBlock("2_Emergent_Circulation", "MAIN", num_bars=8, energy=0.82, has_drums=True, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=980.0, groove_profile="ukg_syncopate", rhythm_patterns=rhythm_climax),
        MacroBlock("3a_Golden_Climax_Rise", "MAIN", num_bars=4, energy=0.99, has_drums=True, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=True, filter_cutoff=1400.0, groove_profile="ukg_syncopate", filter_curve=climax_curve, rhythm_patterns=rhythm_climax),
        MacroBlock("3b_Golden_Ratio_Breath", "MAIN", num_bars=2, energy=0.55, has_drums=False, has_bass=False, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=900.0, groove_profile="ukg_syncopate"),
        MacroBlock("3c_Golden_Climax_Return", "MAIN", num_bars=6, energy=0.99, has_drums=True, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=True, filter_cutoff=1400.0, groove_profile="ukg_syncopate", filter_curve=climax_curve, rhythm_patterns=rhythm_climax),
        MacroBlock("4_Thermodynamic_Cooling", "MAIN", num_bars=6, energy=0.70, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=850.0, groove_profile="ukg_syncopate", rhythm_patterns=rhythm_climax),
        MacroBlock("5_Infinite_Invariance", "MAIN", num_bars=6, energy=0.40, has_drums=False, has_bass=False, has_pad=True, has_stabs=False, has_bells=True, has_vocaloid=False, filter_cutoff=600.0, groove_profile="ukg_syncopate"),
    ]
    
    # Ethereal SuperSaw Choir reinforcement during the Golden Ratio Climax (bars 16 to 28, beats 64 to 112)
    choir_events = []
    for bar in range(16, 28):
        b_start = bar * 4.0
        # Sustained root/fifth/ninth pads on Dbmaj9
        notes = [49, 56, 60, 63] if bar % 4 == 0 else ([58, 61, 65, 68] if bar % 4 == 1 else ([54, 58, 61, 65] if bar % 4 == 2 else [56, 61, 63, 66]))
        for note in notes:
            choir_events.append(NoteEvent(
                midi_note=note,
                start_beat=b_start,
                duration_beats=3.9,
                velocity=0.65
            ))
            
    choir_channel = TrackChannel(
        id="climax_supersaw_choir",
        instrument_id="supersaw",
        events=choir_events,
        fx_chain=[
            FXDef(plugin_type="filter", params={"cutoff_hz": 2600.0, "mode": "lowpass"}),
            FXDef(plugin_type="chorus", params={"rate_hz": 0.8, "depth_ms": 3.0}, mix=0.45),
            FXDef(plugin_type="dimension", params={"width": 1.8, "hp_side_hz": 200.0}),
        ],
        sends={"cathedral_verb": 0.40},
        volume_db=-3.5,
        pan=0.0
    )
    
    send_busses = {
        "cathedral_verb": SendBusDef(
            id="cathedral_verb",
            fx_chain=[
                FXDef(plugin_type="reverb", params={"decay_time_s": 3.4}, mix=1.0),
                FXDef(plugin_type="dimension", params={"width": 1.8, "hp_side_hz": 200.0}),
            ],
            volume_db=-3.5
        )
    }
    master_bus_fx = [
        FXDef(plugin_type="dimension", params={"width": 1.30, "hp_side_hz": 180.0}),
        FXDef(plugin_type="distortion", params={"drive": 1.15, "mode": "tape", "tone": 0.75}, mix=0.18),
        FXDef(plugin_type="transient", params={"attack_db": 0.8, "sustain_db": 0.5}),
    ]
    return Score(
        title="06 The Gauge-Corrected Heart",
        schema_version="2.3",
        seed=606,
        bpm=84.0,
        meter_numerator=4,
        meter_denominator=4,
        key_root="Db",
        scale_type="major",
        groove_profile="ukg_syncopate",
        swing_ratio=0.58,
        drum_kit="ukg",
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[choir_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(target_lufs=-14.8, peak_ceiling_db=-0.8, sidechain_duck_db=4.5),
        metadata={"track_number": 6, "concept": "Gauge-corrected Hamiltonian action E° with macroscopic golden-ratio emotional climax."}
    )


def render_track6_golden_vocal(total_samples: int, sr: int, bpm: float) -> np.ndarray:
    """
    Golden-ratio legato vocal: a single soaring phrase held across the drum dropout
    at bars 20-21 (the phi=0.618 point of the climax), synthesized as one continuous
    glide since TrackChannel/NoteEvent dispatch can't express legato (HARMONIA_WISHLIST.md
    item 9). Mixed into the compiled instrumental as a manual post-process.
    """
    beat_s = 60.0 / bpm
    synth = FormantVocaloidSynth(sr=sr)
    reverb = StudioConvolutionReverb(sr=sr, decay_time_s=4.2, damp_hz=3200.0)
    vocal_track = np.zeros((total_samples, 2), dtype=np.float32)

    # bar 20 = beat 80 at 4/4
    notes = [72, 75, 80, 75]
    durations_beats = [2.0, 1.5, 1.5, 3.0]
    durations_s = [d * beat_s for d in durations_beats]
    phrase = synth.render_legato_phrase(notes, durations_s, vowel='a', velocity=0.75, glide_s=0.12)

    start_sample = int(80.0 * beat_s * sr)
    add_to_track(vocal_track, start_sample, phrase)
    return reverb.process(vocal_track, mix=0.42)


def compile_track_6(studio: HarmoniaStudio, score: Score, art_path: str, prefix: str) -> dict:
    """Compiles Track 6 with the golden-ratio vocal mixed in as a manual post-process."""
    instrumental_wav = os.path.join(ALBUM_DIR, f"{prefix}_instrumental_tmp.wav")
    res = studio.compile_score(score, output_path=instrumental_wav, export_mp3=False,
                                export_stems=False, export_midi=True, export_musicxml=True)

    sr, data = wavfile.read(instrumental_wav)
    instrumental = data.astype(np.float32) / 32767.0

    vocal = render_track6_golden_vocal(len(instrumental), sr, score.bpm)
    if len(vocal) < len(instrumental):
        vocal = np.pad(vocal, ((0, len(instrumental) - len(vocal)), (0, 0)))
    else:
        vocal = vocal[:len(instrumental)]
    vocal_carver = VoicePocketProcessor(config=score.mastering.voice_pocket, sr=sr)
    vocal = vocal_carver.process(vocal)
    mixed = instrumental + vocal * 1.1

    masterer = BroadcastMasteringEngine(config=score.mastering, sr=sr)
    mastered = masterer.master(mixed)
    dithered = apply_tpdf_dither(mastered, bit_depth=16, seed=score.seed)
    int16_out = (np.clip(dithered, -1.0, 1.0) * 32767.0).astype(np.int16)

    wav_path = os.path.join(ALBUM_DIR, f"{prefix}.wav")
    wavfile.write(wav_path, sr, int16_out)

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("MP3 export requires FFmpeg on PATH.")
    mp3_path = os.path.join(ALBUM_DIR, f"{prefix}.mp3")
    subprocess.run([ffmpeg, "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "320k", mp3_path],
                    check=True, capture_output=True)

    # compile_score derived MIDI/MusicXML paths from the temp instrumental filename;
    # rename them to the final track prefix.
    for ext, res_key in ((".mid", "midi"), (".musicxml", "musicxml")):
        tmp_path = os.path.splitext(instrumental_wav)[0] + ext
        final_path = os.path.join(ALBUM_DIR, f"{prefix}{ext}")
        if os.path.exists(tmp_path):
            os.replace(tmp_path, final_path)
            res[res_key] = final_path

    if os.path.exists(instrumental_wav):
        os.remove(instrumental_wav)
    instrumental_manifest = os.path.splitext(instrumental_wav)[0] + ".manifest.json"
    if os.path.exists(instrumental_manifest):
        os.remove(instrumental_manifest)

    import hashlib
    with open(wav_path, "rb") as f:
        render_sha256 = hashlib.sha256(f.read()).hexdigest()
    res["render_sha256"] = render_sha256

    manifest_path = os.path.splitext(wav_path)[0] + ".manifest.json"
    manifest = {
        "manifest_version": "1.0",
        "engine": "harmonia",
        "score_schema_version": score.schema_version,
        "score_fingerprint": res["score_fingerprint"],
        "render_sha256": render_sha256,
        "seed": score.seed,
        "sample_rate": sr,
        "bpm": score.bpm,
        "bars": sum(b.num_bars for b in score.timeline),
        "frames": len(int16_out),
        "channels": 2,
    }
    with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")

    res["wav"] = wav_path
    res["mp3"] = mp3_path
    return res


def compile_track_4(studio: HarmoniaStudio, score: Score, art_path: str, prefix: str) -> dict:
    """
    Compiles Track 4 with continuous dusty vinyl crackle mixed under the final master --
    the one J-Dilla-specific texture on the album, not reused anywhere else.
    """
    wav_path = os.path.join(ALBUM_DIR, f"{prefix}.wav")
    res = studio.compile_score(score, output_path=wav_path, export_mp3=False,
                                export_stems=False, export_midi=True, export_musicxml=True)

    sr, data = wavfile.read(wav_path)
    mastered = data.astype(np.float32) / 32767.0

    drums = HarmoniaDrumEngine(sr=sr)
    vinyl = drums.render_vinyl_texture(duration_s=len(mastered) / sr, level_db=-41.0)
    n = min(len(mastered), len(vinyl))
    combined = mastered.copy()
    combined[:n] += vinyl[:n]

    dithered = apply_tpdf_dither(combined, bit_depth=16, seed=score.seed)
    int16_out = (np.clip(dithered, -1.0, 1.0) * 32767.0).astype(np.int16)
    wavfile.write(wav_path, sr, int16_out)

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("MP3 export requires FFmpeg on PATH.")
    mp3_path = os.path.join(ALBUM_DIR, f"{prefix}.mp3")
    subprocess.run([ffmpeg, "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "320k", mp3_path],
                    check=True, capture_output=True)

    import hashlib
    with open(wav_path, "rb") as f:
        res["render_sha256"] = hashlib.sha256(f.read()).hexdigest()
    res["mp3"] = mp3_path
    return res


def tag_mp3(mp3_path: str, score: Score, art_path: str):
    """Embeds complete ID3 metadata, track numbers, and cover art into the compiled MP3."""
    if not os.path.exists(mp3_path):
        return
        
    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass
        
    track_num = score.metadata.get("track_number", 1)
    clean_title = re.sub(r"^\d+\s+", "", score.title)
    audio.tags.add(TIT2(encoding=3, text=clean_title))
    audio.tags.add(TPE1(encoding=3, text="Harmonia Engine · Gemini 3.8 Flash"))
    audio.tags.add(TPE2(encoding=3, text="Harmonia Engine · Gemini 3.8 Flash"))
    audio.tags.add(TALB(encoding=3, text="Chronosignatures"))
    audio.tags.add(TRCK(encoding=3, text=f"{track_num}/8"))
    audio.tags.add(TDRC(encoding=3, text="2026"))
    audio.tags.add(TCON(encoding=3, text=TRACK_GENRES.get(track_num, "Electronic")))
    audio.tags.add(TCOP(encoding=3, text="© 2026 Harmonia Engine"))
    audio.tags.add(COMM(encoding=3, lang="eng", desc="Description", text=score.metadata.get("concept", "")))

    if os.path.exists(art_path):
        with open(art_path, "rb") as img_f:
            audio.tags.add(APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,  # Cover (front)
                desc="Cover",
                data=img_f.read()
            ))
    audio.save(v2_version=3)
    print(f"  [ID3 Tagged] {mp3_path} with art: {art_path}")


def compile_album():
    tracks = [
        ("01_zero_temperature_limit", build_track_1(), os.path.join(ART_DIR, "01_zero_temperature_limit.jpg")),
        ("02_circulation_on_the_simplex", build_track_2(), os.path.join(ART_DIR, "02_circulation_on_the_simplex.jpg")),
        ("03_noncommutative_horizon", build_track_3(), os.path.join(ART_DIR, "03_noncommutative_horizon.jpg")),
        ("04_the_aitchison_drift", build_track_4(), os.path.join(ART_DIR, "04_the_aitchison_drift.jpg")),
        ("05_cumulant_cascade", build_track_5(), os.path.join(ART_DIR, "05_cumulant_cascade.jpg")),
        ("06_the_gauge_corrected_heart", build_track_6(), os.path.join(ART_DIR, "06_the_gauge_corrected_heart.jpg")),
    ]
    
    studio = HarmoniaStudio()
    album_report = []
    
    print("=== COMPILING CHRONOSIGNATURES ALBUM (HARMONIA v2.3 REMASTER) ===")
    t_start = time.time()
    
    for filename_prefix, score, art_path in tracks:
        print(f"\n---> Processing Track: '{score.title}'")
        # 1. Validate
        ScoreParser.validate(score)
        
        # 2. Save Score JSON
        score_json_path = os.path.join(ALBUM_DIR, f"{filename_prefix}.json")
        ScoreParser.save_to_file(score, score_json_path)
        print(f"  Saved Score IR: {score_json_path}")
        
        # 3. Compile Master Audio & Exports
        wav_path = os.path.join(ALBUM_DIR, f"{filename_prefix}.wav")
        if score.metadata.get("track_number") == 6:
            res = compile_track_6(studio, score, art_path, filename_prefix)
        elif score.metadata.get("track_number") == 4:
            res = compile_track_4(studio, score, art_path, filename_prefix)
        else:
            res = studio.compile_score(
                score,
                output_path=wav_path,
                export_mp3=True,
                export_stems=False,
                export_midi=True,
                export_musicxml=True
            )
        print(f"  Rendered WAV: {wav_path}")
        print(f"  Exported MP3: {res.get('mp3', 'N/A')}")
        print(f"  Exported MIDI: {res.get('midi', 'N/A')}")
        print(f"  Exported MusicXML: {res.get('musicxml', 'N/A')}")
        print(f"  Score Fingerprint: {res['score_fingerprint']}")
        print(f"  Render SHA256: {res['render_sha256']}")
        
        # 4. Embed ID3v2 Tags & APIC Artwork
        if res.get("mp3"):
            tag_mp3(res["mp3"], score, art_path)
        
        # 5. Acoustic Analysis
        acoustic_metrics = studio.analyze_audio_file(wav_path)
        print(f"  [Acoustics] Integrated LUFS: {acoustic_metrics.integrated_lufs_estimate:.2f}, "
              f"Dynamic Range: {acoustic_metrics.dynamic_range_db:.2f} dB, "
              f"True Peak: {acoustic_metrics.true_peak_dbfs:.2f} dBFS, "
              f"Spectral Centroid: {acoustic_metrics.spectral_centroid_hz:.1f} Hz, "
              f"Spectral Rolloff: {acoustic_metrics.spectral_rolloff_hz:.1f} Hz, "
              f"Dissonance Index: {acoustic_metrics.dissonance_index:.3f}")
        
        # 6. Symbolic Analysis
        symbolic_metrics = analyze_score(score)
        
        # 7. Mozart Taylor Probes
        cycle = score.chords["MAIN"]
        mozart_probes = probe_progression(cycle, score.key_root, score.scale_type)
        mozart_summary = [p.to_dict() for p in mozart_probes]
        
        # 8. Signature Report
        sig_report = musical_signature_report(cycle, order=3)
        
        track_data = {
            "title": score.title,
            "filename_prefix": filename_prefix,
            "key_root": score.key_root,
            "scale_type": score.scale_type,
            "bpm": score.bpm,
            "meter": f"{score.meter_numerator}/{score.meter_denominator}",
            "groove_profile": score.groove_profile,
            "seed": score.seed,
            "total_bars": sum(b.num_bars for b in score.timeline),
            "score_fingerprint": res["score_fingerprint"],
            "render_sha256": res["render_sha256"],
            "acoustic": {
                "integrated_lufs": round(float(acoustic_metrics.integrated_lufs_estimate), 2),
                "dynamic_range_db": round(float(acoustic_metrics.dynamic_range_db), 2),
                "true_peak_dbfs": round(float(acoustic_metrics.true_peak_dbfs), 2),
                "spectral_rolloff_hz": round(float(acoustic_metrics.spectral_rolloff_hz), 1),
                "spectral_centroid_hz": round(float(acoustic_metrics.spectral_centroid_hz), 1),
                "dissonance_index": round(float(acoustic_metrics.dissonance_index), 3),
            },
            "symbolic": symbolic_metrics,
            "mozart_probes": mozart_summary,
            "signature_report": sig_report,
            "concept": score.metadata.get("concept", ""),
        }
        album_report.append(track_data)
        
    report_path = os.path.join(REPO_ROOT, "analysis", "album_analysis.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(album_report, f, indent=2)
    print(f"\n=== ALBUM COMPILATION COMPLETE ({time.time() - t_start:.2f}s) ===")
    print(f"Master album analysis report written to: {report_path}")


if __name__ == "__main__":
    compile_album()
