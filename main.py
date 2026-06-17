"""
EPQ Modelling: Can Artificial Gravity Ever Be Truly Replicated in Spacecraft?
Three models demonstrating the physics of rotational artificial gravity.
Each plot can be saved directly from the window that pops up.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# SHARED STYLE SETTINGS
# Makes all three plots look consistent and professional
# ─────────────────────────────────────────────────────────────────────────────

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 2.2,
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
})


# ─────────────────────────────────────────────────────────────────────────────
# MODEL 1: ROTATION RATE vs REQUIRED RADIUS FOR DIFFERENT G-LEVELS
#
# Physics: From a = ω²r, rearranging gives r = a / ω²
# ω is angular velocity in radians per second = (2π × rpm) / 60
# So: r = (g_target × 60²) / (4π² × rpm²) = g_target × 895.8 / rpm²
#
# What this shows: the engineering trade-off. Lower RPM = larger radius.
# Halving the RPM quadruples the radius (inverse square relationship).
# This is why all practical proposals use 3–6 rpm with large radii.
# ─────────────────────────────────────────────────────────────────────────────

fig1, ax1 = plt.subplots(figsize=(10, 6))

rpm_values = np.linspace(0.5, 10, 500)   # rotation rates from 0.5 to 10 RPM
omega = (2 * np.pi * rpm_values) / 60    # convert RPM to radians per second

# Three target gravity levels
g_targets = {
    '1.00g  (Earth)':   (9.81,  '#1a56a0'),   # blue
    '0.50g  (Half Earth)': (4.905, '#e07b00'), # orange
    '0.38g  (Mars surface)': (3.73, '#b5271b'), # red
}

for label, (g, colour) in g_targets.items():
    radius = g / omega**2                 # r = a / ω²
    ax1.plot(rpm_values, radius, colour, label=label)

# Mark the NASA reference design point: 4 rpm, 56 m → 1g
ax1.scatter([4], [56], color='#1a56a0', zorder=5, s=100)
ax1.annotate(
    'NASA reference design\n4 rpm, 56 m → 1g',
    xy=(4, 56), xytext=(5.5, 80),
    arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5),
    fontsize=10, color='#333333'
)

# Shade the "comfortable" zone (2–6 rpm, 15–200 m)
ax1.axvspan(2, 6, alpha=0.08, color='green', label='Comfortable zone (2–6 rpm)')
ax1.axhline(y=200, color='grey', linestyle='--', alpha=0.5, linewidth=1)
ax1.text(0.6, 205, 'Likely impractical above this radius', fontsize=9, color='grey')

ax1.set_xlabel('Rotation Rate (RPM)')
ax1.set_ylabel('Required Radius (metres)')
ax1.set_title('Model 1: Rotation Rate vs Required Radius for Artificial Gravity\n'
              'Higher RPM → smaller (cheaper, lighter) spacecraft — but more Coriolis discomfort')
ax1.set_xlim(0.5, 10)
ax1.set_ylim(0, 250)
ax1.legend(loc='upper right', framealpha=0.9)

# Annotation explaining the inverse square law
ax1.text(7.2, 170,
    'r = g_target / ω²\n'
    'Doubling RPM\nquarters the radius',
    fontsize=9, color='#444444',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9)
)

plt.tight_layout()
plt.savefig('model1_rotation_vs_radius.png', dpi=150, bbox_inches='tight')
print("Model 1 saved as model1_rotation_vs_radius.png")
plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# MODEL 2: GRAVITY GRADIENT vs HABITAT RADIUS
#
# Physics: In a rotating habitat, centripetal acceleration a = ω²r
# varies linearly with radius. A person's head is ~1.8 m closer to the
# axis than their feet, so their head feels less 'gravity' than their feet.
#
# Gradient = (a_feet - a_head) / a_feet × 100%
#           = (ω²r - ω²(r - 1.8)) / ω²r × 100%
#           = 1.8 / r × 100%
#
# Notice ω cancels out entirely — gradient depends only on radius and
# person height, not rotation rate. This is a purely geometric result.
#
# Why this matters: in a true gravitational field, the gradient across
# 1.8 m is negligible (Earth's field varies by ~0.06% across a person).
# In a rotating habitat at small radii, the gradient can be 20%+ — 
# a clear sign that this is NOT the same as true gravity.
# ─────────────────────────────────────────────────────────────────────────────

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(13, 6))

radii = np.linspace(5, 200, 500)     # habitat radii from 5 m to 200 m
person_height = 1.8                  # metres (standard assumption)

gradient_percent = (person_height / radii) * 100   # gradient formula

# Left plot: gradient vs radius
ax2a.plot(radii, gradient_percent, '#1a56a0')

# Threshold lines
ax2a.axhline(y=10, color='orange', linestyle='--', linewidth=1.5,
             label='10% threshold (generally acceptable)')
ax2a.axhline(y=20, color='red', linestyle='--', linewidth=1.5,
             label='20% threshold (uncomfortable)')
ax2a.axhline(y=0.06, color='green', linestyle=':', linewidth=1.5,
             label='Earth surface gradient (~0.06%) — true gravity reference')

# Mark where 10% threshold is met
r_10pct = person_height / 0.10       # = 18 m
ax2a.scatter([r_10pct], [10], color='orange', zorder=5, s=80)
ax2a.annotate(f'r = {r_10pct:.0f} m\n(10% gradient)', xy=(r_10pct, 10),
              xytext=(r_10pct + 15, 18),
              arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2),
              fontsize=9)

# Mark NASA reference (56 m)
gradient_at_56 = (person_height / 56) * 100
ax2a.scatter([56], [gradient_at_56], color='#1a56a0', zorder=5, s=80)
ax2a.annotate(f'NASA design: r = 56 m\nGradient = {gradient_at_56:.1f}%',
              xy=(56, gradient_at_56), xytext=(75, 8),
              arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2),
              fontsize=9)

ax2a.set_xlabel('Habitat Radius (metres)')
ax2a.set_ylabel('Head-to-Foot Gravity Gradient (%)')
ax2a.set_title('Gravity Gradient vs Habitat Radius\n'
               '(independent of rotation rate — purely geometric)')
ax2a.set_xlim(5, 150)
ax2a.set_ylim(0, 40)
ax2a.legend(loc='upper right', fontsize=9)

# Formula box
ax2a.text(95, 30,
    'Gradient = 1.8 / r × 100%\n'
    'ω cancels — geometry only.',
    fontsize=9, color='#444444',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9)
)

# Right plot: visualise gravity at head vs feet for different radii
example_radii = [10, 25, 56, 100]
colours_ex = ['#b5271b', '#e07b00', '#1a56a0', '#2e7d32']
omega_4rpm = (2 * np.pi * 4) / 60   # 4 rpm in rad/s

ax2b.set_xlim(-0.5, len(example_radii) - 0.5)
ax2b.set_ylim(0, 1.3)

for i, (r, col) in enumerate(zip(example_radii, colours_ex)):
    g_feet = omega_4rpm**2 * r / 9.81           # g at feet (normalised)
    g_head = omega_4rpm**2 * (r - 1.8) / 9.81   # g at head (normalised)
    grad = (person_height / r) * 100

    # Draw bar for feet
    ax2b.bar(i, g_feet, width=0.35, color=col, alpha=0.8, align='center')
    # Draw bar for head (darker)
    ax2b.bar(i - 0.18, g_head, width=0.35, color=col, alpha=0.4, align='center')

    ax2b.text(i, g_feet + 0.02, f'{g_feet:.2f}g\n(feet)', ha='center', fontsize=8, color=col)
    ax2b.text(i - 0.18, g_head - 0.12, f'{g_head:.2f}g\n(head)', ha='center', fontsize=8, color='grey')
    ax2b.text(i, 1.18, f'r = {r} m\nΔ = {grad:.0f}%', ha='center', fontsize=8)

ax2b.axhline(y=1.0, color='black', linestyle=':', alpha=0.5, linewidth=1)
ax2b.text(-0.4, 1.01, '1g', fontsize=9, color='black')
ax2b.set_xticks(range(len(example_radii)))
ax2b.set_xticklabels([f'r = {r} m' for r in example_radii])
ax2b.set_ylabel('Gravity Level (g)')
ax2b.set_title('Head vs Foot Gravity at 4 rpm\n(dark bar = feet, light bar = head)')

feet_patch = mpatches.Patch(color='grey', alpha=0.8, label='Gravity at feet')
head_patch = mpatches.Patch(color='grey', alpha=0.3, label='Gravity at head')
ax2b.legend(handles=[feet_patch, head_patch], fontsize=9, loc='lower right')

plt.tight_layout()
plt.savefig('model2_gravity_gradient.png', dpi=150, bbox_inches='tight')
print("Model 2 saved as model2_gravity_gradient.png")
plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# MODEL 3: CORIOLIS FORCE vs ROTATION RATE
#
# Physics: The Coriolis acceleration is ac = 2ω × v
# where ω is angular velocity (rad/s) and v is the velocity of a
# moving object relative to the rotating frame (e.g. a person walking).
#
# We compare this to the artificial gravity level ag = ω²r
# at a given rotation rate (with r chosen to maintain 1g at each ω).
#
# Ratio = ac / ag = 2ωv / ω²r = 2v / ωr
#
# This is the key result: as ω increases, r decreases (to maintain 1g),
# but r decreases faster than ω increases (r ∝ 1/ω²), so:
# Ratio = 2v / ωr = 2v·ω / g_target
# i.e. the Coriolis-to-gravity ratio INCREASES with rotation rate.
# More RPM = more Coriolis relative to artificial gravity.
#
# Stone's threshold: Coriolis force should be <25% of artificial gravity.
# This defines a maximum acceptable rotation rate for a given walking speed.
# ─────────────────────────────────────────────────────────────────────────────

fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(13, 6))

rpm_range = np.linspace(0.5, 12, 500)
omega_range = (2 * np.pi * rpm_range) / 60

g_target = 9.81       # aiming for 1g
radius_1g = g_target / omega_range**2    # required radius to maintain 1g

walking_speeds = {
    'Walking (1.2 m/s)':  (1.2,  '#1a56a0'),
    'Jogging (2.5 m/s)':  (2.5,  '#e07b00'),
    'Head turn (~0.3 m/s)': (0.3, '#2e7d32'),
}

for label, (v, colour) in walking_speeds.items():
    coriolis_acc = 2 * omega_range * v                     # ac = 2ωv
    coriolis_ratio = (coriolis_acc / g_target) * 100       # as % of 1g

    ax3a.plot(rpm_range, coriolis_ratio, colour, label=label)

# Stone's 25% threshold
ax3a.axhline(y=25, color='red', linestyle='--', linewidth=1.8,
             label="Stone's 25% comfort threshold")

# Shade uncomfortable zone
ax3a.fill_between(rpm_range, 25, 200, alpha=0.07, color='red')
ax3a.text(8, 40, 'Uncomfortable zone\n(Coriolis > 25% of g)',
          fontsize=9, color='#b5271b')

# Mark commonly cited 6 rpm limit
ax3a.axvline(x=6, color='purple', linestyle=':', linewidth=1.5,
             label='Historical 6 rpm limit (NASA 1987 standards)')

ax3a.set_xlabel('Rotation Rate (RPM)')
ax3a.set_ylabel('Coriolis Acceleration as % of Artificial Gravity')
ax3a.set_title("Model 3: Coriolis Force vs Rotation Rate\n"
               "Why high RPM habitats cause disorientation")
ax3a.set_xlim(0.5, 12)
ax3a.set_ylim(0, 80)
ax3a.legend(loc='upper left', fontsize=9, framealpha=0.9)

ax3a.text(7.5, 62,
    'ac = 2ωv\n'
    'Ratio = 2v·ω / g\n'
    'Rises linearly with ω.',
    fontsize=9, color='#444444',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9)
)

# Right plot: summary — the three-way trade-off
# Shows radius, Coriolis ratio, and gradient all on one chart (normalised)
ax3b_twin = ax3b.twinx()

radius_norm = radius_1g / radius_1g.max()      # normalised 0–1
gradient_norm = (1.8 / radius_1g) / (1.8 / radius_1g).max()
coriolis_norm = (2 * omega_range * 1.2 / 9.81) / (2 * omega_range * 1.2 / 9.81).max()

line1, = ax3b.plot(rpm_range, radius_1g, '#1a56a0', label='Radius required for 1g (m) — left axis')
line2, = ax3b_twin.plot(rpm_range, (1.8 / radius_1g) * 100, '#e07b00',
                        linestyle='--', label='Gravity gradient % — right axis')
line3, = ax3b_twin.plot(rpm_range, (2 * omega_range * 1.2 / 9.81) * 100, '#b5271b',
                        linestyle=':', label='Coriolis as % of g (walking) — right axis')

ax3b.set_xlabel('Rotation Rate (RPM)')
ax3b.set_ylabel('Habitat Radius (metres)', color='#1a56a0')
ax3b_twin.set_ylabel('Percentage (%)', color='#333333')
ax3b.set_title('The Engineering Trade-Off\n'
               'Smaller habitats (higher RPM) = more Coriolis & less gradient')
ax3b.set_xlim(0.5, 10)
ax3b.set_ylim(0, 220)
ax3b_twin.set_ylim(0, 65)
ax3b.tick_params(axis='y', labelcolor='#1a56a0')

lines = [line1, line2, line3]
labels = [l.get_label() for l in lines]
ax3b.legend(lines, labels, loc='upper right', fontsize=8.5, framealpha=0.9)

# Add vertical line at 4 rpm NASA design point
ax3b.axvline(x=4, color='grey', linestyle=':', alpha=0.7)
ax3b.text(4.1, 190, 'NASA\n4 rpm', fontsize=8.5, color='grey')

plt.tight_layout()
plt.savefig('model3_coriolis_tradeoff.png', dpi=150, bbox_inches='tight')
print("Model 3 saved as model3_coriolis_tradeoff.png")
plt.show()

print("\nAll three models complete.")
print("Three PNG files saved in the same folder as this script.")
print("Open each PNG to view and save for your EPQ.")