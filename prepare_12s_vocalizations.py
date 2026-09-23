# prepare_12s_vocalizations.py
import os
import sys
import io
import json
import zlib
import struct
import wave
import subprocess
import urllib.request
import numpy as np
import scipy.signal
import scipy.ndimage
import imageio_ffmpeg

BASE_DIR = r'C:\Users\Utsav\.gemini\antigravity\scratch\bird_voice_visualization_3d'
DATA_DIR = os.path.join(BASE_DIR, 'data')
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

AUDIO_ZIP_URL = 'https://zenodo.org/records/7505820/files/audio_files.zip?download=1'
AUDIO_CD_OFFSET = 1040925533
AUDIO_CD_SIZE = 201255

print('Loading audio_files.zip central directory...')
req = urllib.request.Request(AUDIO_ZIP_URL, headers={'Range': f'bytes={AUDIO_CD_OFFSET}-{AUDIO_CD_OFFSET + AUDIO_CD_SIZE - 1}'})
cd_data = urllib.request.urlopen(req).read()

pos = 0
audio_entries = {}
while pos < len(cd_data):
    if cd_data[pos:pos+4] != b'PK\x01\x02':
        break
    header = cd_data[pos:pos+46]
    sig, ver_made, ver_need, flags, method, mod_time, mod_date, crc32, comp_size, uncomp_size, name_len, extra_len, comm_len, disk_start, int_attr, ext_attr, local_hdr_offset = struct.unpack('<4sHHHHHHIIIHHHHHII', header)
    name = cd_data[pos+46:pos+46+name_len].decode('utf-8', errors='ignore')
    if name.endswith('.mp3'):
        audio_entries[os.path.basename(name).lower()] = {
            'name': name,
            'comp_size': comp_size,
            'local_hdr_offset': local_hdr_offset,
            'method': method
        }
    pos += 46 + name_len + extra_len + comm_len

print(f'Total audio entries indexed: {len(audio_entries)}')

FEATURED_CONFIG = [
    {
        'species': 'Acrocephalus arundinaceus',
        'common_name': 'Great Reed Warbler',
        'mp3_file': 'XC417157.mp3',
        'start_sec': 0.0,
        'duration_sec': 12.0,
        'category': 'Complex Melodic Song & Trill',
        'color': '#fee440',
        'description': 'Continuous, highly dynamic song featuring rapid trills, rising whistles, and sharp frequency modulations.'
    },
    {
        'species': 'Alcedo atthis',
        'common_name': 'Common Kingfisher',
        'mp3_file': 'XC511677.mp3',
        'start_sec': 1.0,
        'duration_sec': 12.0,
        'category': 'Ultra-High Piercing Whistle',
        'color': '#ff007f',
        'description': 'Series of intense, high-frequency whistle pulses (5 to 8 kHz) cutting through wetland water noise.'
    },
    {
        'species': 'Botaurus stellaris',
        'common_name': 'Great Bittern',
        'mp3_file': 'XC100296.mp3',
        'start_sec': 0.0,
        'duration_sec': 12.0,
        'category': 'Deep Resonant Bass Boom',
        'color': '#00f5d4',
        'description': 'Deep sub-1000 Hz resonant bass booming sequence with slow acoustic envelope pulses.'
    },
    {
        'species': 'Himantopus himantopus',
        'common_name': 'Black-winged Stilt',
        'mp3_file': 'XC500624.mp3',
        'start_sec': 5.0,
        'duration_sec': 12.0,
        'category': 'Staccato Yapping & Pitch Spikes',
        'color': '#9b5de5',
        'description': 'Rapid succession of sharp piping calls featuring steep upward pitch sweeps.'
    },
    {
        'species': 'Dendrocopos minor',
        'common_name': 'Lesser Spotted Woodpecker',
        'mp3_file': 'XC120411.mp3',
        'start_sec': 0.0,
        'duration_sec': 12.0,
        'category': 'Harmonic Piping Call',
        'color': '#f15bb5',
        'description': 'Fast ringing series of high-pitched notes with clean harmonic ladders and steady pitch plateaus.'
    },
    {
        'species': 'Tachybaptus ruficollis',
        'common_name': 'Little Grebe',
        'mp3_file': 'XC134240.mp3',
        'start_sec': 0.0,
        'duration_sec': 12.0,
        'category': 'Whinnying Trill',
        'color': '#00bbf9',
        'description': 'Accelerating laughing trill with high-density frequency fluctuations between 2 and 5 kHz.'
    },
    {
        'species': 'Motacilla flava',
        'common_name': 'Western Yellow Wagtail',
        'mp3_file': 'XC102793.mp3',
        'start_sec': 0.0,
        'duration_sec': 12.0,
        'category': 'Slurred Flight Whistle',
        'color': '#48cae4',
        'description': 'Distinctive two-tone slurred flight calls with clean rising pitch inflection.'
    }
]

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
results = []

for cfg in FEATURED_CONFIG:
    sp_name = cfg['species']
    mp3_file = cfg['mp3_file']
    start_s = cfg['start_sec']
    dur_s = cfg['duration_sec']
    print(f"\nProcessing 12s recording: {cfg['common_name']} ({mp3_file})...")

    key = mp3_file.lower()
    if key not in audio_entries:
        print(f"  Entry not found: {mp3_file}")
        continue

    entry = audio_entries[key]
    fetch_len = 30 + 300 + entry['comp_size']
    req = urllib.request.Request(AUDIO_ZIP_URL, headers={'Range': f'bytes={entry["local_hdr_offset"]}-{entry["local_hdr_offset"] + fetch_len}'})
    raw = urllib.request.urlopen(req).read()
    loc_sig, loc_ver, loc_flags, loc_method, loc_mtime, loc_mdate, loc_crc, loc_csize, loc_usize, loc_nlen, loc_xlen = struct.unpack('<4sHHHHHIIIHH', raw[:30])
    file_data = raw[30 + loc_nlen + loc_xlen : 30 + loc_nlen + loc_xlen + loc_csize]
    decomp = zlib.decompress(file_data, -15) if loc_method == 8 else file_data

    temp_full = os.path.join(AUDIO_DIR, f'temp_{key}')
    with open(temp_full, 'wb') as f:
        f.write(decomp)

    # 1. Output clean 12s MP3 for browser
    out_mp3_name = f'long_{sp_name.replace(" ", "_")}.mp3'
    out_mp3_path = os.path.join(AUDIO_DIR, out_mp3_name)
    cmd_mp3 = [
        ffmpeg, '-y',
        '-ss', str(start_s),
        '-i', temp_full,
        '-t', str(dur_s),
        '-acodec', 'libmp3lame',
        '-b:a', '128k',
        out_mp3_path
    ]
    subprocess.run(cmd_mp3, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 2. Output WAV for high-precision STFT analysis
    temp_wav = os.path.join(AUDIO_DIR, f'temp_{key}.wav')
    cmd_wav = [
        ffmpeg, '-y',
        '-ss', str(start_s),
        '-i', temp_full,
        '-t', str(dur_s),
        '-ar', '22050',
        '-ac', '1',
        temp_wav
    ]
    subprocess.run(cmd_wav, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if os.path.exists(temp_full):
        os.remove(temp_full)

    if not os.path.exists(temp_wav):
        print(f"  Error generating WAV for {sp_name}")
        continue

    # Read WAV data
    with wave.open(temp_wav, 'rb') as wf:
        n_frames = wf.getnframes()
        sr = wf.getframerate()
        raw_bytes = wf.readframes(n_frames)
    os.remove(temp_wav)

    samples = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    actual_dur = len(samples) / sr
    print(f"  Decoded {len(samples)} samples ({actual_dur:.2f}s, sr={sr}Hz)")

    # 3. Compute continuous STFT spectrogram
    # nperseg=1024, noverlap=512 -> dt ~ 23.2ms
    f_axis, t_axis, Sxx = scipy.signal.spectrogram(samples, fs=sr, nperseg=1024, noverlap=512)
    S_db = 10 * np.log10(Sxx + 1e-10)
    S_db -= np.max(S_db) # 0 dB max

    # Filter frequencies 80 Hz to 8500 Hz
    f_mask = (f_axis >= 80) & (f_axis <= 8500)
    f_filt = f_axis[f_mask]
    S_filt_db = S_db[f_mask, :]

    # Peak dominant frequency
    peak_indices = np.argmax(S_filt_db, axis=0)
    peak_f_hz = f_filt[peak_indices]
    peak_f_khz = peak_f_hz / 1000.0
    peak_db = np.max(S_filt_db, axis=0)

    # Smooth peak frequency slightly to reduce STFT quantization jitter
    smooth_f_hz = scipy.signal.medfilt(peak_f_hz, 3)

    # Pitch derivative (Hz / second)
    dt = t_axis[1] - t_axis[0]
    df_dt = np.gradient(smooth_f_hz, dt)

    # 4. Note / Syllable Segmentation
    db_thresh = max(-40.0, float(np.percentile(peak_db, 50)))
    active_mask = (peak_db > db_thresh)
    kernel = np.ones(3, dtype=bool)
    active_mask = scipy.ndimage.binary_dilation(active_mask, structure=kernel)

    notes = []
    in_note = False
    n_start = 0

    for i, is_act in enumerate(active_mask):
        if is_act and not in_note:
            in_note = True
            n_start = i
        elif not is_act and in_note:
            in_note = False
            if (i - n_start) >= 3:
                n_t = t_axis[n_start:i]
                n_f = smooth_f_hz[n_start:i]
                n_db = peak_db[n_start:i]

                delta_f = n_f[-1] - n_f[0]
                slope = delta_f / max(0.02, n_t[-1] - n_t[0])
                f_std = np.std(n_f)

                if slope > 800:
                    tone_type = 'Rising Whistle'
                    symbol = '^'
                    direction = 'rising'
                elif slope < -800:
                    tone_type = 'Falling Slur'
                    symbol = 'v'
                    direction = 'falling'
                elif f_std > 300:
                    tone_type = 'Trill / Warble'
                    symbol = '~'
                    direction = 'oscillating'
                else:
                    tone_type = 'Steady Tone'
                    symbol = '-'
                    direction = 'steady'

                notes.append({
                    'id': len(notes) + 1,
                    'start_time': round(float(n_t[0]), 3),
                    'end_time': round(float(n_t[-1]), 3),
                    'duration_sec': round(float(n_t[-1] - n_t[0]), 3),
                    'mean_freq_khz': round(float(np.mean(n_f) / 1000.0), 2),
                    'min_freq_khz': round(float(np.min(n_f) / 1000.0), 2),
                    'max_freq_khz': round(float(np.max(n_f) / 1000.0), 2),
                    'peak_db': round(float(np.max(n_db)), 1),
                    'tone_type': tone_type,
                    'symbol': symbol,
                    'direction': direction
                })

    print(f"  Detected {len(notes)} discrete notes/tones across {actual_dur:.1f}s!")

    # 5. High-resolution trajectory time-series
    trajectory = []
    for i in range(len(t_axis)):
        curr_t = float(t_axis[i])
        active_note = next((n for n in notes if n['start_time'] <= curr_t <= n['end_time']), None)
        slope_val = float(df_dt[i])

        if slope_val > 600:
            trend = 'rising'
        elif slope_val < -600:
            trend = 'falling'
        else:
            trend = 'steady'

        trajectory.append({
            'time': round(curr_t, 3),
            'freq_khz': round(float(smooth_f_hz[i] / 1000.0), 3),
            'db': round(float(peak_db[i]), 1),
            'is_voice': bool(active_mask[i]),
            'note_id': active_note['id'] if active_note else None,
            'note_type': active_note['tone_type'] if active_note else None,
            'pitch_trend': trend,
            'slope_hz_s': round(slope_val, 1)
        })

    # 6. 3D surface mesh: downsample for smooth 60fps WebGL (120 time x 40 freq)
    step_t = max(1, len(t_axis) // 120)
    step_f = max(1, len(f_filt) // 40)
    mesh_z = S_filt_db[::step_f, ::step_t]
    mesh_t = t_axis[::step_t]
    mesh_f_khz = f_filt[::step_f] / 1000.0

    results.append({
        'species': sp_name,
        'common_name': cfg['common_name'],
        'category': cfg['category'],
        'color': cfg['color'],
        'description': cfg['description'],
        'duration_sec': round(actual_dur, 2),
        'audio_url': f'audio/{out_mp3_name}',
        'notes_count': len(notes),
        'notes': notes,
        'trajectory': trajectory,
        'mesh': {
            'time': [round(float(t), 3) for t in mesh_t],
            'freq_khz': [round(float(f), 3) for f in mesh_f_khz],
            'z_db': [[round(float(v), 1) for v in row] for row in mesh_z.tolist()]
        }
    })

out_json = os.path.join(DATA_DIR, 'bird_vocalizations_12s.json')
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({
        'dataset': 'Western Mediterranean Wetlands Bird Dataset (Zenodo 7505820)',
        'duration_mode': '12_seconds_continuous',
        'species_count': len(results),
        'species': results
    }, f, indent=2)

print(f"\nPipeline finished! Exported {len(results)} long recordings to {out_json}")
