# generate_3d_plots.py
import os
import json
import plotly.graph_objects as go

BASE_DIR = r'C:\Users\Utsav\.gemini\antigravity\scratch\bird_voice_visualization_3d'
DATA_PATH = os.path.join(BASE_DIR, 'data', 'bird_vocalizations_12s.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

SPECIES_PALETTE = {
    'Great Reed Warbler': {'rgb': (245, 197, 24), 'name': 'Great Reed Warbler (Song)'},        # Golden Yellow
    'Common Kingfisher': {'rgb': (91, 142, 245), 'name': 'Common Kingfisher (Whistle)'},       # Soft Blue
    'Great Bittern': {'rgb': (180, 134, 107), 'name': 'Great Bittern (Bass Boom)'},           # Earthy Brown/Tan
    'Black-winged Stilt': {'rgb': (248, 113, 113), 'name': 'Black-winged Stilt (Yapping)'},    # Warm Coral Red
    'Lesser Spotted Woodpecker': {'rgb': (253, 230, 138), 'name': 'Woodpecker (Piping)'},     # Cream Yellow
    'Little Grebe': {'rgb': (249, 115, 22), 'name': 'Little Grebe (Trill)'},                   # Warm Orange
    'Western Yellow Wagtail': {'rgb': (147, 197, 253), 'name': 'Yellow Wagtail (Flight)'}      # Sky Blue
}

def create_image2_point_cloud(output_file):
    fig = go.Figure()

    for sp in dataset['species']:
        cname = sp['common_name']
        pal = SPECIES_PALETTE.get(cname, {'rgb': (120, 120, 120), 'name': cname})
        rgb = pal['rgb']
        traj = sp['trajectory']

        times = [p['time'] for p in traj]
        freqs_hz = [p['freq_khz'] * 1000.0 for p in traj]
        dbs = [p['db'] for p in traj]

        # Confidence opacity: dimmer points are less certain
        colors = [
            f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {max(0.12, min(0.95, (db + 60.0) / 45.0)):.2f})'
            for db in dbs
        ]

        fig.add_trace(go.Scatter3d(
            x=times,
            y=freqs_hz,
            z=dbs,
            mode='markers',
            marker=dict(
                size=4.5,
                color=colors,
                line=dict(width=0)
            ),
            name=pal['name'],
            hovertemplate=(
                f"<b>{cname}</b><br>"
                "Time (X): %{x:.2f}s<br>"
                "Frequency (Y): %{y:.0f} Hz<br>"
                "Energy (Z): %{z:.1f} dB<extra></extra>"
            )
        ))

    # Exact layout from Image 2
    fig.update_layout(
        paper_bgcolor='#fafaf8',
        plot_bgcolor='#fafaf8',
        title=dict(
            text=(
                "<b>Avian Acoustic Point Cloud (Voice Frequency vs Energy)</b><br>"
                "<span style='font-size:12px; color:#64748b; font-weight:normal;'>"
                "Point opacity encodes the pitch model's confidence for that frame — dimmer points are less certain"
                "</span>"
            ),
            font=dict(family='Segoe UI, Arial, sans-serif', size=16, color='#1e293b'),
            x=0.04,
            y=0.96
        ),
        scene=dict(
            xaxis=dict(
                title=dict(text='X', font=dict(size=14, color='#334155')),
                backgroundcolor='#ffffff',
                gridcolor='#ebece9',
                showbackground=True,
                zerolinecolor='#cbd5e1',
                tickfont=dict(size=11, color='#64748b'),
                showspikes=False
            ),
            yaxis=dict(
                title=dict(text='Y', font=dict(size=14, color='#334155')),
                range=[0, 8500],
                backgroundcolor='#ffffff',
                gridcolor='#ebece9',
                showbackground=True,
                zerolinecolor='#cbd5e1',
                tickvals=[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
                tickfont=dict(size=11, color='#64748b'),
                showspikes=False
            ),
            zaxis=dict(
                title=dict(text='Z', font=dict(size=14, color='#334155')),
                range=[-65, -5],
                backgroundcolor='#ffffff',
                gridcolor='#ebece9',
                showbackground=True,
                zerolinecolor='#cbd5e1',
                tickvals=[-60, -50, -40, -30, -20, -10],
                tickfont=dict(size=11, color='#64748b'),
                showspikes=False
            ),
            camera=dict(
                eye=dict(x=-1.65, y=-1.55, z=1.15),
                center=dict(x=0, y=0, z=-0.15)
            ),
            aspectratio=dict(x=1.35, y=1.25, z=0.85)
        ),
        legend=dict(
            x=0.03,
            y=0.88,
            font=dict(family='Segoe UI, Arial, sans-serif', size=11, color='#334155'),
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        margin=dict(l=10, r=10, t=70, b=30)
    )

    fig.write_html(output_file)
    print(f"Exported: {output_file}")

if __name__ == '__main__':
    create_image2_point_cloud(os.path.join(BASE_DIR, 'multi_species_comparison_3d.html'))
    create_image2_point_cloud(os.path.join(BASE_DIR, 'point_cloud_3d.html'))
    print("Point cloud plots generated successfully!")
