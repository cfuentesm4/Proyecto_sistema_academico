from datetime import date


# =====================================================================
# CLASE BASE: contiene lo que comparten todos los modelos
# =====================================================================
class ModeloBase:
    """Clase padre de los modelos del sistema."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    # Convierte un diccionario en un objeto de la clase correspondiente.
    # Este método se escribe una sola vez y lo heredan las clases hijas.
    @classmethod
    def desde_diccionario(cls, datos):
        datos = dict(datos)
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    # Convierte los datos básicos del objeto en un diccionario.
    def a_diccionario(self):
        return {"id": self.id}

    # Cada clase hija puede personalizar la forma de mostrarse.
    def etiqueta(self):
        return f"registro {self.id}"

    # Permite mostrar el objeto directamente con print().
    def __str__(self):
        return f"[{self.id}] {self.etiqueta()}"


# =====================================================================
# CLASE PERSONA: contiene los datos comunes de una persona
# =====================================================================
class Persona(ModeloBase):
    """Clase padre para las personas del sistema."""

    def __init__(self, id_registro, nombre, apellido, email):
        # Reutilizamos el constructor de ModeloBase para guardar el id.
        super().__init__(id_registro)

        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    # Devuelve el nombre y el apellido juntos.
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    # Agrega los datos de Persona al diccionario heredado.
    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


# =====================================================================
# MODELO DE ESTUDIANTES
# =====================================================================
class Estudiante(Persona):
    """Un estudiante es una persona que tiene carnet y carrera."""

    def __init__(self, id_registro, nombre, apellido, email,
                 carnet="", carrera=""):

        # Heredamos los datos comunes de Persona.
        super().__init__(id_registro, nombre, apellido, email)

        # Agregamos los datos propios del estudiante.
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self):
        # Recuperamos los datos de Persona y añadimos los del estudiante.
        datos = super().a_diccionario()
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        # Personalizamos la forma en que se muestra cada estudiante.
        return (
            f"{self.nombre_completo()} · "
            f"{self.carnet} · {self.carrera}"
        )


# =====================================================================
# MODELO DE MATERIAS
# =====================================================================
class Materia(ModeloBase):
    """Representa una materia y controla sus cupos disponibles."""

    # Estos valores son compartidos por todas las materias.
    CUPOS_MAXIMOS = 30
    NOTA_APROBACION = 14

    def __init__(self, id_registro, nombre, codigo,
                 creditos=0, cupos=0):

        super().__init__(id_registro)

        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    # Comprueba que una nota esté dentro del rango de 0 a 20.
    @staticmethod
    def es_nota_valida(valor):
        try:
            nota = float(valor)
            return 0 <= nota <= 20
        except (TypeError, ValueError):
            return False

    # Indica si todavía existen cupos disponibles.
    def hay_cupo(self):
        return self.cupos > 0

    # Descuenta un cupo cuando se registra una matrícula.
    def ocupar_cupo(self):
        if self.hay_cupo():
            self.cupos -= 1
            return True
        return False

    # Devuelve un cupo cuando se retira una matrícula.
    def liberar_cupo(self):
        if self.cupos < Materia.CUPOS_MAXIMOS:
            self.cupos += 1
            return True
        return False

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.codigo
        datos["creditos"] = self.creditos
        datos["cupos"] = self.cupos
        return datos

    def etiqueta(self):
        return (
            f"{self.nombre} · {self.codigo} · "
            f"{self.creditos} créditos · "
            f"{self.cupos} cupos disponibles"
        )


# =====================================================================
# MODELO DE MATRÍCULAS
# =====================================================================
class Matricula(ModeloBase):
    """Relaciona a un estudiante con una materia."""

    def __init__(self, id_registro, estudiante_id, materia_id,
                 periodo, nota=None, fecha=""):

        super().__init__(id_registro)

        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo

        # Si todavía no se registra una nota, queda como None.
        self.nota = None if nota is None else float(nota)

        # Si no se proporciona una fecha, se utiliza la fecha actual.
        self.fecha = fecha or date.today().isoformat()

    # Comprueba si la matrícula tiene una nota aprobatoria.
    def esta_aprobada(self):
        return (
            self.nota is not None
            and self.nota >= Materia.NOTA_APROBACION
        )

    # Devuelve el estado de la matrícula según la nota registrada.
    def estado(self):
        if self.nota is None:
            return "Pendiente"
        if self.esta_aprobada():
            return "Aprobada"
        return "Reprobada"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["nota"] = self.nota
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        nota_mostrar = (
            f"{self.nota:.2f}" if self.nota is not None
            else "Sin nota"
        )

        return (
            f"Estudiante {self.estudiante_id} · "
            f"Materia {self.materia_id} · "
            f"Periodo {self.periodo} · "
            f"Nota: {nota_mostrar} · {self.estado()}"
        )