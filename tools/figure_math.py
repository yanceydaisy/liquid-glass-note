"""Exact geometric figures and a sampling-only diagnostic for the guide.

The grid figure evaluates the production v5 displacement formula at t = 0.
It is not a WebGL screenshot or a complete glass material renderer.
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw


def round_box(x, y, width, height, corner):
    qx = np.abs(x - width / 2) - (width / 2 - corner)
    qy = np.abs(y - height / 2) - (height / 2 - corner)
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - corner


def radial_boundary(rx, ry, width, height, corner):
    corner = min(corner, width / 2, height / 2)
    norm = np.maximum(np.hypot(rx, ry), 0.0001)
    dx, dy = np.abs(rx) / norm, np.abs(ry) / norm
    tx = (width / 2) / np.maximum(dx, 0.0001)
    ty = (height / 2) / np.maximum(dy, 0.0001)
    side = np.minimum(tx, ty)
    cx, cy = width / 2 - corner, height / 2 - corner
    q = dx * cx + dy * cy
    disc = np.maximum(0, q * q - cx * cx - cy * cy + corner * corner)
    curved = np.maximum(1, q + np.sqrt(disc))
    return np.where((dx * side > cx) & (dy * side > cy), curved, np.maximum(1, side))


def smoothstep(lo, hi, x):
    t = np.clip((x - lo) / (hi - lo), 0, 1)
    return t * t * (3 - 2 * t)


def sampling_offsets(x, y, width, height, corner, time=0.0):
    rx, ry = x - width / 2, y - height / 2
    radius_to_edge = radial_boundary(rx, ry, width, height, corner)
    px, py = rx / radius_to_edge, ry / radius_to_edge
    ang = np.arctan2(py, px)
    shape = 15 / 100 * .09 * .25
    wave = shape * (.40 * np.sin(3 * ang + time * 1.7) + .28 * np.sin(5 * ang - time * 1.1))
    rr = np.clip(np.hypot(px, py) / (1 + wave), 0, 1)
    refract = 26 * 1.36
    wave_lens = .4 * np.sin(ang * 5 + time * .75) * rr ** 2
    sh = (.65 * np.maximum(0, 1 - rr * rr) ** .75 - .20 * rr ** 6 + wave_lens * .035) * refract
    gain = smoothstep(.05, .97, rr)
    strength = (.052 + .12 * gain) * refract
    wx = np.sin(py * 3.1 + px * 1.4 + time * .18) * np.cos(px * 2.2)
    wy = np.cos(px * 3.4 - py * 1.3 - time * .15) * np.sin(py * 2.1 + .8)
    return px * sh + wx * strength, py * sh + wy * strength


def build_refraction_figures(directory):
    directory = Path(directory)
    width, height, corner, scale = 260, 150, 20, 3
    nw, nh = width * scale, height * scale
    source = Image.new('RGB', (nw, nh), '#e7ecee')
    draw = ImageDraw.Draw(source)
    for x in range(0, width + 1, 20):
        draw.line((x * scale, 0, x * scale, nh), fill='#8299aa', width=2 * scale)
    for y in range(0, height + 1, 20):
        draw.line((0, y * scale, nw, y * scale), fill='#8299aa', width=2 * scale)
    draw.line((130 * scale, 0, 130 * scale, nh), fill='#9e6273', width=3 * scale)
    draw.line((0, 75 * scale, nw, 75 * scale), fill='#243d50', width=3 * scale)
    pixels = np.asarray(source, dtype=float)
    yy, xx = np.mgrid[:nh, :nw]
    x, y = (xx + .5) / scale, (yy + .5) / scale
    sx, sy = sampling_offsets(x, y, width, height, corner)
    # Texture UV uses bottom-left origin; conversion back to image coordinates
    # makes both pixel-space shifts positive here, matching the shader's -dy.
    u = np.clip((x + sx) / width, .001, .999)
    v = np.clip((y + sy) / height, .001, .999)
    tx, ty = np.clip(u * nw - .5, 0, nw - 1), np.clip(v * nh - .5, 0, nh - 1)
    x0, y0 = np.floor(tx).astype(int), np.floor(ty).astype(int)
    x1, y1 = np.minimum(x0 + 1, nw - 1), np.minimum(y0 + 1, nh - 1)
    ax, ay = (tx - x0)[..., None], (ty - y0)[..., None]
    sampled = (pixels[y0, x0] * (1 - ax) * (1 - ay) + pixels[y0, x1] * ax * (1 - ay)
               + pixels[y1, x0] * (1 - ax) * ay + pixels[y1, x1] * ax * ay)
    mask = (1 - smoothstep(-.8, .8, round_box(x, y, width, height, corner)))[..., None]
    paper = np.array([244, 244, 241])
    for name, data in [('refraction-source.png', pixels), ('refraction-sampling.png', sampled)]:
        Image.fromarray(np.round(data * mask + paper * (1 - mask)).astype('uint8')).save(directory / name)
    # A true displacement field changes its local scale; a crop/translation
    # would have constant offset. Keep this figure honest during rebuilds.
    assert np.ptp(sx) > 5 and np.ptp(sy) > 5


def validate_geometry():
    errors = []
    for width, height, corner in [(248, 110, 30), (190, 108, 31), (260, 150, 20)]:
        angles = np.linspace(-math.pi, math.pi, 721)
        dx, dy = np.cos(angles), np.sin(angles)
        r = radial_boundary(dx, dy, width, height, corner)
        errors.append(np.max(np.abs(round_box(width / 2 + dx * r, height / 2 + dy * r, width, height, corner))))
    assert max(errors) < 1e-8, errors
    return max(errors)


if __name__ == '__main__':
    print('Max ray-boundary SDF error:', validate_geometry())
    build_refraction_figures(Path(__file__).resolve().parents[1] / 'assets')
