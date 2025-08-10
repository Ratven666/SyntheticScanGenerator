import trimesh
import numpy as np

# Создаём тор
mesh = trimesh.creation.torus(10, 5)

# Задаём случайные цвета для каждого полигона
colors = np.random.randint(0, 255, (len(mesh.faces), 4), dtype=np.uint8)
colors[:, 3] = 255  # Альфа = 255 (непрозрачность)
mesh.visual.face_colors = colors

# Проверяем
print("Тип цветов:", mesh.visual.kind)  # Должно быть 'face'
print("Пример цветов:", mesh.visual.face_colors[:3])

# Экспортируем
mesh.export("torus_colored.ply")  # PLY сохранит цвета
mesh.show()  # Откроет 3D-просмотрщик