"""
EPQ Modelling: Can Artificial Gravity Ever Be Truly Replicated in Spacecraft?
Four models on the physics of rotational artificial gravity.

CHANGES FROM v1:
  - Model 2: Earth surface gradient corrected from 0.06% to 5.65e-5%.
    The old value divided by Earth's radius in KILOMETRES (6371) against a
    height in METRES (1.8), a factor-of-1000 unit error. The left panel is
    now log-scaled so the corrected Earth reference is actually visible.
  - All models now print the exact figures quoted in the essay, so every
    number in the text can be traced to a line of output.
  - Model 4 added: short-arm intermittent centrifuge vs whole-vehicle
    rotation, showing the two designs fail different physical constraints.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams.update({
    'font.family': ['Arial', 'Liberation Sans', 'DejaVu Sans'],
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

G_EARTH = 9.81          # ms^-2
PERSON_HEIGHT = 1.8     # m
EARTH_RADIUS = 6.371e6  # m  <-- METRES. This is the line that was wrong.


def omega_from_rpm(n):
    """Angular velocity in rad/s from rotation rate in rpm."""
    return 2 * np.pi * n / 60


def rpm_from_omega(w):
    return w * 60 / (2 * np.pi)


# ---------------------------------------------------------------------------
# MODEL 1: ROTATION RATE vs REQUIRED RADIUS
# r = g / omega^2, so r = 895 / n^2 for 1g with n in rpm.
# ---------------------------------------------------------------------------

fig1, ax1 = plt.subplots(figsize=(10, 6))

rpm_values = np.linspace(0.5, 10, 500)
omega = omega_from_rpm(rpm_values)

g_targets = {
    '1.00g  (Earth)': (9.81, '#1a56a0'),
    '0.50g  (Half Earth)': (4.905, '#e07b00'),
    '0.38g  (Mars surface)': (3.73, '#b5271b'),
}

for label, (g, colour) in g_targets.items():
    ax1.plot(rpm_values, g / omega**2, colour, label=label)

ax1.scatter([4], [G_EARTH / omega_from_rpm(4)**2], color='#1a56a0', zorder=5, s=100)
ax1.annotate('NASA reference design\n4 rpm, 56 m \u2192 1g',
             xy=(4, 56), xytext=(5.5, 80),
             arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5),
             fontsize=10, color='#333333')

ax1.axvspan(2, 6, alpha=0.08, color='green', label='Comfortable zone (2\u20136 rpm)')
ax1.axhline(y=200, color='grey', linestyle='--', alpha=0.5, linewidth=1)
ax1.text(0.6, 205, 'Likely impractical above this radius', fontsize=9, color='grey')

ax1.set_xlabel('Rotation Rate (RPM)')
ax1.set_ylabel('Required Radius (metres)')
ax1.set_title('Model 1: Rotation Rate vs Required Radius for Artificial Gravity\n'
              'Higher RPM \u2192 smaller (cheaper, lighter) spacecraft, but more Coriolis discomfort')
ax1.set_xlim(0.5, 10)
ax1.set_ylim(0, 250)
ax1.legend(loc='upper right', framealpha=0.9)
ax1.text(7.2, 170, 'r = g / \u03c9\u00b2\nDoubling RPM\nquarters the radius',
         fontsize=9, color='#444444',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor='#cccccc', alpha=0.9))

plt.tight_layout()
plt.savefig('model1_rotation_vs_radius.png', dpi=150, bbox_inches='tight')
plt.close(fig1)

print("MODEL 1 -- figures quoted in section 3.1")
for n in (1, 4, 6):
    print(f"  {n} rpm -> {G_EARTH / omega_from_rpm(n)**2:7.1f} m for 1g")


# ---------------------------------------------------------------------------
# MODEL 2: GRAVITY GRADIENT vs HABITAT RADIUS
#
# Gradient = (a_feet - a_head) / a_feet = (omega^2 r - omega^2 (r-1.8)) / omega^2 r
#          = 1.8 / r
# omega cancels: the gradient is purely geometric.
#
# Earth reference: g falls off as 1/r^2, so the fractional change over a
# height h is approximately 2h / R_earth = 2(1.8) / 6.371e6 = 5.65e-5 %.
# NOT 0.06%. The old figure used 6371 (km) instead of 6.371e6 (m).
# ---------------------------------------------------------------------------

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(13, 6))

radii = np.linspace(5, 200, 500)
gradient_percent = (PERSON_HEIGHT / radii) * 100
earth_gradient = 2 * PERSON_HEIGHT / EARTH_RADIUS * 100

ax2a.plot(radii, gradient_percent, '#1a56a0')
ax2a.set_yscale('log')

ax2a.axhline(y=10, color='orange', linestyle='--', linewidth=1.5,
             label='10% threshold (generally acceptable)')
ax2a.axhline(y=20, color='red', linestyle='--', linewidth=1.5,
             label='20% threshold (uncomfortable)')
ax2a.axhline(y=earth_gradient, color='green', linestyle=':', linewidth=1.8,
             label=f'Earth surface gradient ({earth_gradient:.1e}%), true gravity')

r_10pct = PERSON_HEIGHT / 0.10
ax2a.scatter([r_10pct], [10], color='orange', zorder=5, s=80)
ax2a.annotate(f'r = {r_10pct:.0f} m\n(10% gradient)', xy=(r_10pct, 10),
              xytext=(r_10pct + 20, 30),
              arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2), fontsize=9)

gradient_at_56 = (PERSON_HEIGHT / 56) * 100
ax2a.scatter([56], [gradient_at_56], color='#1a56a0', zorder=5, s=80)
ax2a.annotate(f'NASA design: r = 56 m\nGradient = {gradient_at_56:.1f}%',
              xy=(56, gradient_at_56), xytext=(80, 0.6),
              arrowprops=dict(arrowstyle='->', color='#333333', lw=1.2), fontsize=9)

ax2a.annotate('', xy=(150, gradient_at_56), xytext=(150, earth_gradient),
              arrowprops=dict(arrowstyle='<->', color='#555555', lw=1.4))
ax2a.text(155, 0.02, 'almost five\norders of\nmagnitude', fontsize=8.5, color='#555555')

ax2a.set_xlabel('Habitat Radius (metres)')
ax2a.set_ylabel('Head-to-Foot Gravity Gradient (%, log scale)')
ax2a.set_title('Gravity Gradient vs Habitat Radius\n'
               '(independent of rotation rate, purely geometric)')
ax2a.set_xlim(5, 200)
ax2a.set_ylim(1e-5, 100)
ax2a.legend(loc='lower left', fontsize=8.5)
ax2a.text(95, 25, 'Gradient = 1.8 / r \u00d7 100%\n\u03c9 cancels, geometry only.',
          fontsize=9, color='#444444',
          bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor='#cccccc', alpha=0.9))

example_radii = [10, 25, 56, 100]
colours_ex = ['#b5271b', '#e07b00', '#1a56a0', '#2e7d32']
omega_4rpm = omega_from_rpm(4)

ax2b.set_xlim(-0.6, len(example_radii) - 0.4)
ax2b.set_ylim(0, 2.15)   # 100 m at 4 rpm gives 1.79g, so headroom is needed

for i, (r, col) in enumerate(zip(example_radii, colours_ex)):
    g_feet = omega_4rpm**2 * r / G_EARTH
    g_head = omega_4rpm**2 * (r - PERSON_HEIGHT) / G_EARTH
    grad = (PERSON_HEIGHT / r) * 100
    ax2b.bar(i, g_feet, width=0.32, color=col, alpha=0.85, align='center')
    ax2b.bar(i - 0.20, g_head, width=0.32, color=col, alpha=0.35, align='center')
    ax2b.text(i + 0.04, g_feet + 0.03, f'{g_feet:.2f}g\n(feet)', ha='left',
              fontsize=8, color=col)
    ax2b.text(i - 0.38, g_head + 0.03, f'{g_head:.2f}g\n(head)', ha='right',
              fontsize=8, color='grey')
    ax2b.text(i - 0.10, 1.95, f'r = {r} m\n\u0394 = {grad:.0f}%', ha='center', fontsize=8)

ax2b.axhline(y=1.0, color='black', linestyle=':', alpha=0.5, linewidth=1)
ax2b.text(-0.55, 1.03, '1g (target)', fontsize=9)
ax2b.set_xticks(range(len(example_radii)))
ax2b.set_xticklabels([f'r = {r} m' for r in example_radii])
ax2b.set_ylabel('Gravity Level (g)')
ax2b.set_title('Head vs Foot Gravity at 4 rpm\n(solid bar = feet, faded bar = head)')
ax2b.legend(handles=[mpatches.Patch(color='grey', alpha=0.85, label='Gravity at feet'),
                     mpatches.Patch(color='grey', alpha=0.35, label='Gravity at head')],
            fontsize=9, loc='lower right')

plt.tight_layout()
plt.savefig('model2_gravity_gradient.png', dpi=150, bbox_inches='tight')
plt.close(fig2)

print("\nMODEL 2 -- figures quoted in section 3.2")
print(f"  gradient at r = 10 m : {1.8/10*100:.1f}%")
print(f"  gradient at r = 56 m : {1.8/56*100:.2f}%")
print(f"  Earth surface        : {earth_gradient:.2e}%  <-- CORRECTED (was 0.06%)")
print(f"  ratio NASA : Earth   : {(1.8/56*100)/earth_gradient:,.0f} times larger")


# ---------------------------------------------------------------------------
# MODEL 3: CORIOLIS FORCE vs ROTATION RATE
# ratio = a_c / g = 2 omega v / g, rising linearly with omega.
# ---------------------------------------------------------------------------

fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(13, 6))

rpm_range = np.linspace(0.5, 12, 500)
omega_range = omega_from_rpm(rpm_range)
radius_1g = G_EARTH / omega_range**2

speeds = {
    'Walking (1.2 m/s)': (1.2, '#1a56a0'),
    'Jogging (2.5 m/s)': (2.5, '#e07b00'),
    'Head turn (~0.3 m/s)': (0.3, '#2e7d32'),
}

for label, (v, colour) in speeds.items():
    ax3a.plot(rpm_range, (2 * omega_range * v / G_EARTH) * 100, colour, label=label)

ax3a.axhline(y=25, color='red', linestyle='--', linewidth=1.8,
             label="Stone's 25% comfort threshold")
ax3a.fill_between(rpm_range, 25, 200, alpha=0.07, color='red')
ax3a.text(8, 45, 'Uncomfortable zone\n(Coriolis > 25% of g)', fontsize=9, color='#b5271b')
ax3a.axvline(x=6, color='purple', linestyle=':', linewidth=1.5,
             label='Historical 6 rpm limit')

for v, colour in ((1.2, '#1a56a0'), (2.5, '#e07b00')):
    n_cross = rpm_from_omega(0.25 * G_EARTH / (2 * v))
    ax3a.scatter([n_cross], [25], color=colour, zorder=6, s=70)
    ax3a.annotate(f'{n_cross:.1f} rpm', xy=(n_cross, 25), xytext=(n_cross - 0.2, 28),
                  fontsize=8.5, color=colour, ha='right')

ax3a.set_xlabel('Rotation Rate (RPM)')
ax3a.set_ylabel('Coriolis Acceleration as % of Artificial Gravity')
ax3a.set_title('Model 3: Coriolis Force vs Rotation Rate\nWhy high RPM habitats cause disorientation')
ax3a.set_xlim(0.5, 12)
ax3a.set_ylim(0, 80)
ax3a.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax3a.text(7.5, 62, 'a_c = 2\u03c9v\nRatio = 2v\u03c9 / g\nRises linearly with \u03c9.',
          fontsize=9, color='#444444',
          bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor='#cccccc', alpha=0.9))

ax3b_twin = ax3b.twinx()
line1, = ax3b.plot(rpm_range, radius_1g, '#1a56a0', label='Radius required for 1g (m), left axis')
line2, = ax3b_twin.plot(rpm_range, (PERSON_HEIGHT / radius_1g) * 100, '#e07b00',
                        linestyle='--', label='Gravity gradient %, right axis')
line3, = ax3b_twin.plot(rpm_range, (2 * omega_range * 1.2 / G_EARTH) * 100, '#b5271b',
                        linestyle=':', label='Coriolis as % of g (walking), right axis')

ax3b.set_xlabel('Rotation Rate (RPM)')
ax3b.set_ylabel('Habitat Radius (metres)', color='#1a56a0')
ax3b_twin.set_ylabel('Percentage (%)')
ax3b.set_title('The Engineering Trade-Off\nSmaller habitats (higher RPM) = more Coriolis, less gradient')
ax3b.set_xlim(0.5, 10)
ax3b.set_ylim(0, 220)
ax3b_twin.set_ylim(0, 65)
ax3b.tick_params(axis='y', labelcolor='#1a56a0')
ax3b.legend([line1, line2, line3], [l.get_label() for l in (line1, line2, line3)],
            loc='upper right', fontsize=8.5, framealpha=0.9)
ax3b.axvline(x=4, color='grey', linestyle=':', alpha=0.7)
ax3b.text(4.1, 190, 'NASA\n4 rpm', fontsize=8.5, color='grey')

plt.tight_layout()
plt.savefig('model3_coriolis_tradeoff.png', dpi=150, bbox_inches='tight')
plt.close(fig3)

print("\nMODEL 3 -- figures quoted in section 3.3")
for n in (4, 8):
    print(f"  walking at {n} rpm : {2*omega_from_rpm(n)*1.2/G_EARTH*100:.1f}% of g")
print(f"  jogging at 4 rpm  : {2*omega_from_rpm(4)*2.5/G_EARTH*100:.1f}% of g")
for v, name in ((1.2, 'walking'), (2.5, 'jogging'), (0.3, 'head turn')):
    print(f"  {name:9s} crosses 25% at {rpm_from_omega(0.25*G_EARTH/(2*v)):5.1f} rpm")


# ---------------------------------------------------------------------------
# MODEL 4 (NEW): SHORT-ARM INTERMITTENT CENTRIFUGE vs WHOLE-VEHICLE ROTATION
#
# Both designs deliver 1g at the feet. Sweeping radius from 1 m to 200 m and
# setting omega so that omega^2 r = g at every point, the two constraints move
# in opposite directions:
#
#   gravity gradient  = 1.8 / r          -> punishing at small r
#   Coriolis ratio    = 2 v omega / g    -> punishing at large omega (small r)
#                                           but only if the subject MOVES
#
# The short-arm design escapes the Coriolis constraint because the subject is
# supine and passive, so v is a head turn, not a walking pace. What it cannot
# escape is the gradient: at r = 2 m the head sits at 0.10g while the feet sit
# at 1g. The two designs therefore fail different physical constraints, which
# is the point the new section of the essay needs to make.
# ---------------------------------------------------------------------------

fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(13, 6))

r_sweep = np.logspace(0, np.log10(200), 600)
omega_sweep = np.sqrt(G_EARTH / r_sweep)

grad_sweep = PERSON_HEIGHT / r_sweep * 100
cor_walk = 2 * omega_sweep * 1.2 / G_EARTH * 100
cor_head = 2 * omega_sweep * 0.3 / G_EARTH * 100

ax4a.plot(r_sweep, grad_sweep, '#e07b00', linestyle='--', label='Gravity gradient (%)')
ax4a.plot(r_sweep, cor_walk, '#b5271b', linestyle=':', label='Coriolis, walking (% of g)')
ax4a.plot(r_sweep, cor_head, '#2e7d32', label='Coriolis, head turn only (% of g)')
ax4a.axhline(y=25, color='red', linestyle='--', alpha=0.6, linewidth=1.4)
ax4a.text(1.1, 28, "Stone's 25% limit", fontsize=8.5, color='#b5271b')
ax4a.axhline(y=10, color='orange', linestyle='--', alpha=0.6, linewidth=1.4)
ax4a.text(1.1, 11, '10% gradient limit', fontsize=8.5, color='#e07b00')

ax4a.axvspan(1.5, 3.0, alpha=0.10, color='#2e7d32')
ax4a.text(2.1, 170, 'Short-arm\ncentrifuge\n17\u201322 rpm', fontsize=9,
          color='#2e7d32', ha='center')
ax4a.axvspan(25, 100, alpha=0.10, color='#1a56a0')
ax4a.text(50, 170, 'Whole-vehicle rotation\n3\u20136 rpm', fontsize=9,
          color='#1a56a0', ha='center')

ax4a.set_xscale('log')
ax4a.set_yscale('log')
ax4a.set_xlim(1, 200)
ax4a.set_ylim(0.5, 300)
ax4a.set_xlabel('Radius delivering 1g at the feet (metres, log scale)')
ax4a.set_ylabel('Constraint magnitude (%, log scale)')
ax4a.set_title('Model 4: Two Designs, Two Different Constraints\n'
               'Both deliver 1g at the feet; neither escapes both limits')
ax4a.legend(loc='lower left', fontsize=8.5, framealpha=0.9)

designs = ['Short-arm\nr = 2.5 m\n18.9 rpm', 'Compact ring\nr = 25 m\n6.0 rpm',
           'NASA design\nr = 56 m\n4.0 rpm']
design_r = [2.5, 25, 56]
x = np.arange(len(designs))
width = 0.27

grad_vals = [PERSON_HEIGHT / r * 100 for r in design_r]
walk_vals = [2 * np.sqrt(G_EARTH / r) * 1.2 / G_EARTH * 100 for r in design_r]
head_vals = [2 * np.sqrt(G_EARTH / r) * 0.3 / G_EARTH * 100 for r in design_r]

b1 = ax4b.bar(x - width, grad_vals, width, color='#e07b00', label='Gravity gradient')
b2 = ax4b.bar(x, walk_vals, width, color='#b5271b', label='Coriolis, walking')
b3 = ax4b.bar(x + width, head_vals, width, color='#2e7d32', label='Coriolis, head turn')

for bars in (b1, b2, b3):
    for bar in bars:
        ax4b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.10,
                  f'{bar.get_height():.0f}%', ha='center', fontsize=8)

ax4b.axhline(y=25, color='red', linestyle='--', alpha=0.6, linewidth=1.4)
ax4b.text(2.42, 27, "Stone's 25% limit", fontsize=8, color='#b5271b', ha='right')
ax4b.set_yscale('log')
ax4b.set_ylim(1, 400)
ax4b.set_xticks(x)
ax4b.set_xticklabels(designs, fontsize=9)
ax4b.set_ylabel('% (log scale)')
ax4b.set_title('The Same Trade-Off as a Direct Comparison\n'
               'Short-arm wins on Coriolis only because the subject does not walk')
ax4b.legend(fontsize=8.5, loc='upper right')

plt.tight_layout()
plt.savefig('model4_shortarm_vs_wholevehicle.png', dpi=150, bbox_inches='tight')
plt.close(fig4)

print("\nMODEL 4 -- figures for the new alternatives section")
for r in (2.0, 2.5, 3.0, 25.0, 56.0):
    n = rpm_from_omega(np.sqrt(G_EARTH / r))
    print(f"  r = {r:5.1f} m -> {n:5.1f} rpm | gradient {PERSON_HEIGHT/r*100:5.1f}% | "
          f"head sees {(r-PERSON_HEIGHT)/r:.2f}g | Coriolis walk "
          f"{2*np.sqrt(G_EARTH/r)*1.2/G_EARTH*100:5.1f}% | head turn "
          f"{2*np.sqrt(G_EARTH/r)*0.3/G_EARTH*100:5.1f}%")

print("\nAll four models complete. Four PNG files saved.")
