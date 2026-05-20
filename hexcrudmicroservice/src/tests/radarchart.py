import matplotlib.pyplot as plt
import numpy as np
#c0c0c0 fondo
# Configuración de los ejes
categories = ['Performance', 'Developer\nProductivity', 'Maintainability']

N = len(categories)

# Ángulos para cada eje (en radianes)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # Cerrar el polígono

# Datos: [Performance, Productivity, Maintainability] - escala 0-5
data = {
    'C/C++':     [5, 2, 3],
    'Python':    [2, 5, 4],
    'Rust':      [5, 3, 4],
    'Java':      [4, 5, 5]
}

# Configurar el gráfico polar
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Colores por lenguaje
colors = {'Java': '#32cd32', 'Python': '#3776AB', 'Rust': '#000000', 'C/C++': '#ff0000'}

# Plotear cada lenguaje
for lang, values in data.items():
    values += values[:1]  # Cerrar el polígono
    ax.plot(angles, values, 'o-', linewidth=5, label=lang, color=colors[lang])
    ax.fill(angles, values, alpha=0.2, color=colors[lang])

# Configurar ejes
ax.set_theta_offset(np.pi / 2)  # 2 para empezar desde arriba
ax.set_theta_direction(-1)      # Sentido horario
ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=11, fontweight='bold')

# Escala radial (0 a 5)
ax.set_rlabel_position(0)
plt.yticks([1, 2, 3, 4, 5], [str(i) for i in range(1, 6)], color="black", size=9)
plt.ylim(0, 5)

# Título y leyenda
plt.title('Comparativa de Lenguajes - Backend Stack\n       El por qué Netflix usa Java.', size=16, y=1.05, fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=True)


# Grid y estilo
ax.grid(True, alpha=0.4)
plt.tight_layout()
#plt.savefig('radar_backend.png', dpi=300, bbox_inches='tight')
plt.show()
