"""
CHRONOSIGNATURES: The K-Pop & Pseudo-Collab Remix Suite (Harmonia Engine v2.3)
1. Cumulant Cascade (Gesaffelstein Cyber-Industrial Remix) - Dark EBM / Industrial Techno
2. Cumulant Cascade (LE SSERAFIM Style) - Chic High-Octane K-Pop Dembow
"""

import os
import json
import time
from mutagen.mp3 import MP3
import re
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TPE2, TALB, TRCK, TDRC, TCON, TCOP, COMM

TRACK_GENRES = {
    7: "Industrial Techno / EBM",
    8: "K-Pop / Dembow",
}

from harmonia.ir.schema import (
    Score, ChordDef, MacroBlock, MasteringConfig, TrackChannel, SendBusDef, FXDef, NoteEvent
)
from harmonia.ir.parser import ScoreParser
from harmonia.tools.api import HarmoniaStudio

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMIX_DIR = os.path.join(REPO_ROOT, "tracks")
ART_DIR = os.path.join(REPO_ROOT, "art")


def build_gesaffelstein_remix() -> Score:
    """
    Remix 1: Gesaffelstein Cyber-Industrial Remix (Dark Midtempo Industrial / French EBM Techno)
    Acoustic DNA:
    - 106 BPM 4-on-the-floor heavy TR-909 kick with clean sub weight and driving offbeat hats.
    - Roland TB-303 Acid Diode Bass with dark lowpass filtering (420 Hz), staccato syncopation, and warm diode drive.
    - Pockets of silence: kick downbeats remain open for maximum physical punch; zero clashing stems.
    - Haunting, atmospheric vocal echoes through vintage tape saturation and dark gated room reflections.
    - Master bus analog tape warmth with gentle glue dynamics (no harsh transient clipping).
    """
    chords = [
        ChordDef("Am9", bass_midi=33, pad_notes=[45, 48, 52, 55, 59], stab_notes=[57, 60, 64], bell_notes=[69, 72, 76], vocal_notes=[69, 64]),
        ChordDef("D9", bass_midi=38, pad_notes=[45, 50, 54, 57, 60], stab_notes=[57, 62, 66], bell_notes=[66, 69, 74], vocal_notes=[74, 69]),
        ChordDef("Fmaj7", bass_midi=29, pad_notes=[41, 45, 48, 52, 57], stab_notes=[53, 57, 60], bell_notes=[65, 69, 72], vocal_notes=[69, 65]),
        ChordDef("E7#9", bass_midi=28, pad_notes=[40, 44, 47, 50, 55], stab_notes=[52, 56, 59, 64], bell_notes=[64, 68, 71], vocal_notes=[71, 64]),
    ]
    
    # Hypnotic 4-on-the-floor industrial beats with snappy TR-909 claps and driving offbeat hats
    rhythm_industrial = {
        "kick":  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        "snare": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "hat":   [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    }
    
    # Minimalist, brooding timeline: NO bells, NO competing stabs, NO clashing legacy bass during drops!
    timeline = [
        MacroBlock("1_Monolith_Awakening", "MAIN", num_bars=8, energy=0.55, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=False, filter_cutoff=480.0, groove_profile="straight"),
        MacroBlock("2_Cyber_Industrial_Assault", "MAIN", num_bars=12, energy=0.92, has_drums=True, has_bass=False, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=False, filter_cutoff=650.0, groove_profile="straight", rhythm_patterns=rhythm_industrial),
        MacroBlock("3_Hypnotic_Void", "MAIN", num_bars=6, energy=0.48, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=False, filter_cutoff=420.0, groove_profile="straight"),
        MacroBlock("4_Climactic_Overdrive", "MAIN", num_bars=12, energy=0.98, has_drums=True, has_bass=False, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=False, filter_cutoff=720.0, groove_profile="straight", rhythm_patterns=rhythm_industrial),
        MacroBlock("5_Brutal_Outro", "MAIN", num_bars=6, energy=0.40, has_drums=False, has_bass=True, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=False, filter_cutoff=400.0, groove_profile="straight"),
    ]
    
    # 1. Acid Diode Bass channel: Staccato syncopated motif with intentional breathing space
    acid_events = []
    # Drop 1 (bars 8-20, beats 32-80) & Drop 2 (bars 26-38, beats 104-152)
    for bar_range in [(8, 20), (26, 38)]:
        for bar in range(bar_range[0], bar_range[1]):
            b_start = bar * 4.0
            root = 33 if (bar % 4) == 0 else (38 if (bar % 4) == 1 else (29 if (bar % 4) == 2 else 28))
            
            # Syncopated rhythm leaving space for the kick on beats 1.0, 2.0, 3.0, 4.0
            if bar % 4 == 0:  # Am9 (root A1 = 33)
                acid_events.extend([
                    NoteEvent(midi_note=33, start_beat=b_start + 0.0, duration_beats=0.35, velocity=0.95),
                    NoteEvent(midi_note=33, start_beat=b_start + 1.5, duration_beats=0.25, velocity=0.85),
                    NoteEvent(midi_note=33, start_beat=b_start + 2.5, duration_beats=0.25, velocity=0.88),
                    NoteEvent(midi_note=45, start_beat=b_start + 3.5, duration_beats=0.35, velocity=0.92),  # Octave leap
                ])
            elif bar % 4 == 1:  # D9 (root D2 = 38)
                acid_events.extend([
                    NoteEvent(midi_note=38, start_beat=b_start + 0.0, duration_beats=0.35, velocity=0.95),
                    NoteEvent(midi_note=38, start_beat=b_start + 1.5, duration_beats=0.25, velocity=0.85),
                    NoteEvent(midi_note=38, start_beat=b_start + 2.5, duration_beats=0.25, velocity=0.88),
                    NoteEvent(midi_note=50, start_beat=b_start + 3.25, duration_beats=0.25, velocity=0.90),
                    NoteEvent(midi_note=38, start_beat=b_start + 3.75, duration_beats=0.22, velocity=0.90),
                ])
            elif bar % 4 == 2:  # Fmaj7 (root F1 = 29)
                acid_events.extend([
                    NoteEvent(midi_note=29, start_beat=b_start + 0.0, duration_beats=0.35, velocity=0.95),
                    NoteEvent(midi_note=29, start_beat=b_start + 1.5, duration_beats=0.25, velocity=0.85),
                    NoteEvent(midi_note=29, start_beat=b_start + 2.5, duration_beats=0.25, velocity=0.88),
                    NoteEvent(midi_note=41, start_beat=b_start + 3.5, duration_beats=0.35, velocity=0.92),
                ])
            else:  # E7#9 (root E1 = 28)
                acid_events.extend([
                    NoteEvent(midi_note=28, start_beat=b_start + 0.0, duration_beats=0.35, velocity=0.95),
                    NoteEvent(midi_note=28, start_beat=b_start + 1.5, duration_beats=0.25, velocity=0.85),
                    NoteEvent(midi_note=34, start_beat=b_start + 2.25, duration_beats=0.25, velocity=0.88),  # Tritone tension
                    NoteEvent(midi_note=40, start_beat=b_start + 3.0, duration_beats=0.30, velocity=0.90),
                    NoteEvent(midi_note=28, start_beat=b_start + 3.5, duration_beats=0.35, velocity=0.92),
                ])
            
    acid_channel = TrackChannel(
        id="acid_diode_bass",
        instrument_id="acid_bass",
        events=acid_events,
        fx_chain=[
            FXDef(plugin_type="filter", params={"cutoff_hz": 420.0, "resonance": 2.2, "mode": "lowpass", "envelope_mod": 0.45}),
            FXDef(plugin_type="distortion", params={"drive": 2.4, "mode": "diode", "tone": 0.42}, mix=0.70),
        ],
        sends={"industrial_room": 0.18},
        volume_db=0.0,
        pan=0.0
    )
    
    # 2. Vocal Cyborg channel: Atmospheric, haunting French electro vocal phrases
    vocal_events = []
    for bar in [20, 22, 24, 30, 32, 34]:
        b_start = bar * 4.0
        vocal_events.extend([
            NoteEvent(midi_note=69, start_beat=b_start + 0.5, duration_beats=0.6, velocity=0.85),
            NoteEvent(midi_note=64, start_beat=b_start + 1.75, duration_beats=0.4, velocity=0.80),
            NoteEvent(midi_note=71, start_beat=b_start + 3.0, duration_beats=0.7, velocity=0.88),
        ])
        
    vocal_channel = TrackChannel(
        id="vocal_cyborg_glitch",
        instrument_id="vocaloid",
        events=vocal_events,
        fx_chain=[
            FXDef(plugin_type="distortion", params={"drive": 1.8, "mode": "tape", "tone": 0.50}, mix=0.35),
            # EBM vocal character comes from real signal degradation, not just saturation.
            FXDef(plugin_type="bitcrusher", params={"bit_depth": 6.0, "downsample_factor": 2}, mix=0.35),
            FXDef(plugin_type="filter", params={"cutoff_hz": 2600.0, "mode": "lowpass"}),
            FXDef(plugin_type="chorus", params={"rate_hz": 0.6, "depth_ms": 2.5}, mix=0.35),
        ],
        sends={"industrial_room": 0.45},
        volume_db=-3.5,
        pan=-0.15
    )
    
    # 3. Industrial Transitions: sub-impact intro, tension risers into drops, room downlifters
    transition_events = [
        # Opening sub-impact (midi <= 36 -> render_sub_impact)
        NoteEvent(midi_note=30, start_beat=0.0, duration_beats=2.0, velocity=0.88),
        # Tension riser into Drop 1 (bars 6-8, midi >= 60 -> render_riser)
        NoteEvent(midi_note=60, start_beat=20.0, duration_beats=8.0, velocity=0.80),
        # Downlifter at Drop 1 climax peak (midi <= 48 -> render_downlifter)
        NoteEvent(midi_note=36, start_beat=32.0, duration_beats=3.0, velocity=0.82),
        # Tension riser into Drop 2 (bars 22-26)
        NoteEvent(midi_note=60, start_beat=88.0, duration_beats=8.0, velocity=0.90),
        # Sub-impact re-entry into Drop 2
        NoteEvent(midi_note=30, start_beat=104.0, duration_beats=2.0, velocity=0.95),
    ]
    trans_channel = TrackChannel(
        id="industrial_transitions",
        instrument_id="transitions",
        events=transition_events,
        fx_chain=[
            FXDef(plugin_type="distortion", params={"drive": 1.4, "mode": "tape", "tone": 0.55}, mix=0.20),
        ],
        sends={"industrial_room": 0.25},
        volume_db=-2.0,
        pan=0.0
    )
    
    send_busses = {
        "industrial_room": SendBusDef(
            id="industrial_room",
            fx_chain=[
                FXDef(plugin_type="gated_reverb", params={"threshold_db": -26.0, "hold_ms": 75.0, "release_ms": 20.0}),
                FXDef(plugin_type="filter", params={"cutoff_hz": 2400.0, "mode": "lowpass"}),
            ],
            volume_db=-6.0
        )
    }
    
    master_bus_fx = [
        # Soft highpass below the kick's fundamental: keeps punch while clearing sub mud
        # for a "glassy, hollowed-out" character rather than boomy.
        FXDef(plugin_type="filter", params={"cutoff_hz": 38.0, "resonance": 0.7, "mode": "highpass"}),
        FXDef(plugin_type="distortion", params={"drive": 1.18, "mode": "tape", "tone": 0.70}, mix=0.18),
        FXDef(plugin_type="transient", params={"attack_db": 0.6, "sustain_db": -0.4}),
    ]
    
    return Score(
        title="07 Cumulant Cascade (Gesaffelstein Cyber-Industrial Style)",
        schema_version="2.3",
        seed=808,
        bpm=106.0,
        meter_numerator=4,
        meter_denominator=4,
        key_root="A",
        scale_type="dorian",
        groove_profile="straight",
        swing_ratio=0.50,
        drum_kit="909_industrial",
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[acid_channel, vocal_channel, trans_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        mastering=MasteringConfig(target_lufs=-14.2, peak_ceiling_db=-0.8, sidechain_duck_db=4.2),
        metadata={
            "track_number": 7,
            "remix_style": "Dark Cyber-Industrial / EBM Techno",
            "ghost_collaborator": "Gesaffelstein",
            "concept": "Obsidian acid diode basslines, heavy four-on-the-floor TR-909 kicks, driving offbeat hats, and dark concrete room reflections."
        }
    )


def build_lesserafim_remix() -> Score:
    """
    Remix 2: LE SSERAFIM-Style Dembow Flip (High-Octane K-Pop Dance / Dembow Afrobeat)
    Acoustic DNA:
    - 110 BPM authentic Dembow rhythm with 3-3-2 syncopation.
    - Crisp woody rimshots and tight 16th-note shaker layers.
    - Massive 7-voice detuned SuperSaw brass stabs with Dimension Expander hyper-wide stereo field.
    - Glitched vocal hooks and accelerating tempo-synced transition risers.
    - Modern pop punch via transient shaping and subtle tape master warmth.
    """
    chords = [
        ChordDef("Am9", bass_midi=45, pad_notes=[57, 60, 64, 67, 71], stab_notes=[60, 64, 67, 72], bell_notes=[69, 72, 76, 81], vocal_notes=[76, 72]),
        ChordDef("D9", bass_midi=50, pad_notes=[57, 62, 66, 69, 72], stab_notes=[62, 66, 69, 74], bell_notes=[66, 69, 74, 78], vocal_notes=[74, 69]),
        ChordDef("Fmaj7", bass_midi=41, pad_notes=[53, 57, 60, 64, 69], stab_notes=[57, 60, 64, 69], bell_notes=[65, 69, 72, 77], vocal_notes=[72, 65]),
        ChordDef("E7#9", bass_midi=40, pad_notes=[52, 56, 59, 62, 67], stab_notes=[56, 59, 62, 68], bell_notes=[64, 68, 71, 76], vocal_notes=[75, 68]),
    ]
    
    # Signature LE SSERAFIM-style Dembow syncopation:
    # Kick: 1, 7, 11, 14 (3-3-2 beat grid); Snare/Rimshot: 4, 7, 12
    rhythm_antifragile = {
        "kick":  [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        "snare": [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        "hat":   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    }
    
    timeline = [
        # has_stabs/has_bells off during the two drop sections below: the SuperSaw
        # brass channel owns that register there.
        MacroBlock("1_Catwalk_Intro", "MAIN", num_bars=6, energy=0.70, has_drums=False, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=True, filter_cutoff=850.0, groove_profile="ukg_syncopate"),
        MacroBlock("2_Antifragile_Build", "MAIN", num_bars=8, energy=0.88, has_drums=True, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=1150.0, groove_profile="ukg_syncopate", rhythm_patterns=rhythm_antifragile),
        MacroBlock("3_The_Fearless_Drop", "MAIN", num_bars=12, energy=0.98, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=True, filter_cutoff=1380.0, groove_profile="ukg_syncopate", rhythm_patterns=rhythm_antifragile),
        MacroBlock("4_Chic_Breakdown", "MAIN", num_bars=6, energy=0.68, has_drums=False, has_bass=True, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=True, filter_cutoff=900.0, groove_profile="ukg_syncopate"),
        MacroBlock("5_Grand_Dance_Break", "MAIN", num_bars=12, energy=1.00, has_drums=True, has_bass=True, has_pad=True, has_stabs=False, has_bells=False, has_vocaloid=True, filter_cutoff=1450.0, groove_profile="ukg_syncopate", rhythm_patterns=rhythm_antifragile),
        MacroBlock("6_Sassy_Outro", "MAIN", num_bars=4, energy=0.50, has_drums=False, has_bass=False, has_pad=True, has_stabs=True, has_bells=True, has_vocaloid=False, filter_cutoff=750.0, groove_profile="ukg_syncopate"),
    ]
    
    # 1. SuperSaw Brass Stabs: stadium K-Pop synth brass hitting Dembow syncopations
    saw_events = []
    # Drop 1 (bars 14-26, beats 56.0 to 104.0) & Drop 2 (bars 32-44, beats 128.0 to 176.0)
    for bar_ranges in [(14, 26), (32, 44)]:
        for bar in range(bar_ranges[0], bar_ranges[1]):
            b_start = bar * 4.0
            # Dembow brass accents on beats 0.0, 1.5, 2.75, 3.5
            ch_notes = [57, 60, 64, 69] if bar % 2 == 0 else [57, 62, 66, 71]
            for beat_off, dur in [(0.0, 0.4), (1.5, 0.35), (2.75, 0.3), (3.5, 0.4)]:
                for note in ch_notes:
                    saw_events.append(NoteEvent(
                        midi_note=note,
                        start_beat=b_start + beat_off,
                        duration_beats=dur,
                        velocity=0.92
                    ))
                    
    saw_channel = TrackChannel(
        id="kpop_supersaw_brass",
        instrument_id="supersaw",
        events=saw_events,
        fx_chain=[
            FXDef(plugin_type="chorus", params={"rate_hz": 1.7, "depth_ms": 3.6, "feedback": 0.25}, mix=0.55),
            FXDef(plugin_type="dimension", params={"width": 1.9, "hp_side_hz": 240.0}),
            FXDef(plugin_type="filter", params={"cutoff_hz": 4500.0, "resonance": 1.5, "mode": "lowpass"}),
        ],
        sends={"pop_hall": 0.28, "pingpong": 0.22},
        volume_db=0.0,
        pan=0.1
    )
    
    # 2. Vocal Hook Lead channel: bright melodic K-Pop vocal hooks.
    # Pitches (peak, landing tone, passing tone) follow each chord's own
    # vocal_notes/pad_notes rather than one fixed absolute shape.
    vocal_events = []
    for bar in [0, 1, 2, 3, 14, 15, 18, 19, 26, 27, 28, 29, 34, 35, 38, 39]:
        chord = chords[bar % len(chords)]
        top = chord.vocal_notes[0]
        low = chord.vocal_notes[1]
        passing = chord.pad_notes[1] + 12
        echo = top - 12
        b_start = bar * 4.0
        vocal_events.extend([
            NoteEvent(midi_note=low, start_beat=b_start + 0.0, duration_beats=0.75, velocity=0.90),
            NoteEvent(midi_note=passing, start_beat=b_start + 1.0, duration_beats=0.50, velocity=0.85),
            NoteEvent(midi_note=echo, start_beat=b_start + 1.75, duration_beats=0.50, velocity=0.88),
            NoteEvent(midi_note=top, start_beat=b_start + 2.5, duration_beats=1.00, velocity=0.94),
        ])
        
    vocal_channel = TrackChannel(
        id="vocal_hook_lead",
        instrument_id="vocaloid",
        events=vocal_events,
        fx_chain=[
            FXDef(plugin_type="chorus", params={"rate_hz": 1.4, "depth_ms": 2.2}, mix=0.35),
            FXDef(plugin_type="filter", params={"cutoff_hz": 5800.0, "mode": "lowpass"}),
        ],
        sends={"pop_hall": 0.38, "pingpong": 0.30},
        volume_db=-1.5,
        pan=-0.1
    )
    
    # 3. Transition Sweeper: risers into drop 1 (bars 6-14) and drop 2 (bars 28-32)
    trans_events = [
        NoteEvent(midi_note=60, start_beat=24.0, duration_beats=8.0, velocity=0.85),
        NoteEvent(midi_note=60, start_beat=48.0, duration_beats=8.0, velocity=0.95),
        NoteEvent(midi_note=60, start_beat=120.0, duration_beats=8.0, velocity=1.00),
    ]
    trans_channel = TrackChannel(
        id="pop_transitions",
        instrument_id="transitions",
        events=trans_events,
        fx_chain=[
            FXDef(plugin_type="filter", params={"cutoff_hz": 7800.0, "mode": "lowpass"}),
        ],
        sends={"pop_hall": 0.35},
        volume_db=-1.0,
        pan=0.0
    )
    
    send_busses = {
        "pop_hall": SendBusDef(
            id="pop_hall",
            fx_chain=[
                FXDef(plugin_type="reverb", params={"decay_time_s": 2.4}, mix=1.0),
                FXDef(plugin_type="dimension", params={"width": 1.6, "hp_side_hz": 250.0}),
            ],
            volume_db=-4.0
        ),
        "pingpong": SendBusDef(
            id="pingpong",
            fx_chain=[
                FXDef(plugin_type="delay", params={"delay_time_s": 0.272, "feedback": 0.36, "damp_hz": 4200.0}, mix=1.0),
            ],
            volume_db=-4.5
        )
    }
    
    master_bus_fx = [
        FXDef(plugin_type="dimension", params={"width": 1.35, "hp_side_hz": 200.0}),
        FXDef(plugin_type="transient", params={"attack_db": 1.8, "sustain_db": -0.4}),
        FXDef(plugin_type="distortion", params={"drive": 1.15, "mode": "tape"}, mix=0.20),
    ]

    return Score(
        title="08 Cumulant Cascade (LE SSERAFIM Style)",
        schema_version="2.3",
        seed=909,
        bpm=110.0,
        meter_numerator=4,
        meter_denominator=4,
        key_root="A",
        scale_type="dorian",
        groove_profile="ukg_syncopate",
        swing_ratio=0.58,
        drum_kit="dembow_kpop",
        chords={"MAIN": chords},
        timeline=timeline,
        track_channels=[saw_channel, vocal_channel, trans_channel],
        send_busses=send_busses,
        master_bus_fx=master_bus_fx,
        # Peak ceiling matched to Track 07's for consistent dynamics.
        mastering=MasteringConfig(target_lufs=-14.0, peak_ceiling_db=-0.8, tape_warmth_enabled=True, sidechain_duck_db=4.5),
        metadata={
            "track_number": 8,
            "remix_style": "K-Pop Dance / Afrobeat Dembow",
            "ghost_collaborator": "LE SSERAFIM",
            "concept": "Fearless Afro-Latin Dembow syncopation, 7-voice detuned SuperSaw brass stabs, hyper-wide Haas spatialization, and radiant pop energy."
        }
    )


def tag_mp3(mp3_path: str, score: Score, art_path: str):
    """Embeds complete ID3 metadata, track numbers, and cover art into the compiled MP3."""
    if not os.path.exists(mp3_path):
        return
        
    audio = MP3(mp3_path, ID3=ID3)
    try:
        audio.add_tags()
    except Exception:
        pass
        
    track_num = score.metadata.get("track_number", 7)
    clean_title = re.sub(r"^\d+\s+", "", score.title).replace(" - ", " – ")
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


def compile_remixes():
    remixes = [
        (
            "05_cumulant_cascade_gesaffelstein_remix",
            build_gesaffelstein_remix(),
            os.path.join(ART_DIR, "05_cumulant_cascade_gesaffelstein_remix.jpg")
        ),
        (
            "05_cumulant_cascade_lesserafim_remix",
            build_lesserafim_remix(),
            os.path.join(ART_DIR, "05_cumulant_cascade_lesserafim_remix.jpg")
        ),
    ]
    
    studio = HarmoniaStudio()
    reports = []
    
    print("=== COMPILING K-POP & PSEUDO-COLLAB REMIXES (HARMONIA v2.3) ===")
    t_start = time.time()
    
    for prefix, score, art_path in remixes:
        print(f"\n---> Rendering Remix: '{score.title}'")
        ScoreParser.validate(score)
        
        json_path = os.path.join(REMIX_DIR, f"{prefix}.json")
        ScoreParser.save_to_file(score, json_path)
        print(f"  Saved Score IR: {json_path}")
        
        wav_path = os.path.join(REMIX_DIR, f"{prefix}.wav")
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
        print(f"  Exported MIDI: {res.get('midi')}")
        print(f"  Exported MusicXML: {res.get('musicxml')}")
        
        # Embed ID3 Tags & Art
        if res.get("mp3"):
            tag_mp3(res["mp3"], score, art_path)
            
        acoustic = studio.analyze_audio_file(wav_path)
        print(f"  [Acoustics] LUFS: {acoustic.integrated_lufs_estimate:.2f}, "
              f"Dynamic Range: {acoustic.dynamic_range_db:.2f} dB, "
              f"True Peak: {acoustic.true_peak_dbfs:.2f} dBFS, "
              f"Spectral Centroid: {acoustic.spectral_centroid_hz:.1f} Hz, "
              f"Rolloff: {acoustic.spectral_rolloff_hz:.1f} Hz")
        
        reports.append({
            "title": score.title,
            "prefix": prefix,
            "bpm": score.bpm,
            "meter": f"{score.meter_numerator}/{score.meter_denominator}",
            "drum_kit": score.drum_kit,
            "lufs": round(float(acoustic.integrated_lufs_estimate), 2),
            "dynamic_range_db": round(float(acoustic.dynamic_range_db), 2),
            "true_peak": round(float(acoustic.true_peak_dbfs), 2),
            "spectral_centroid_hz": round(float(acoustic.spectral_centroid_hz), 1),
            "spectral_rolloff_hz": round(float(acoustic.spectral_rolloff_hz), 1),
            "metadata": score.metadata
        })
        
    out_rep = os.path.join(REPO_ROOT, "analysis", "remixes_report.json")
    with open(out_rep, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)
    print(f"\n=== REMIX COMPILATION COMPLETE ({time.time() - t_start:.2f}s) ===")


if __name__ == "__main__":
    compile_remixes()
