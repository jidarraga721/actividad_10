# TODO: Implementa el código del ejercicio aquí
from abc import ABC, abstractmethod
from validadorclave.modelo import errores

class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    @abstractmethod
    def es_valida(self, clave):
        pass

    def _validar_longitud(self, clave):
        if len(clave) <= self._longitud_esperada:
            raise errores.LongitudError("La longitud de la clave no es suficiente.")

    def _contiene_mayuscula(self, clave):
        if not any(c.isupper() for c in clave):
            raise errores.MayusculaError("La clave no contiene mayúsculas.")

    def _contiene_minuscula(self, clave):
        if not any(c.islower() for c in clave):
            raise errores.MinusculaError("La clave no contiene minúsculas.")

    def _contiene_numero(self, clave):
        if not any(c.isdigit() for c in clave):
            raise errores.NumeroError("La clave no contiene números.")

class ReglaValidacionGanimedes(ReglaValidacion):
    def contiene_caracter_especial(self, clave):
        if not any(c in '@_#$%' for c in clave):
            raise errores.CaracterEspecialError("La clave no contiene caracteres especiales.")

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_caracter_especial(clave)
        return True

class ReglaValidacionCalisto(ReglaValidacion):
    def contiene_calisto(self, clave):
        calisto_variations = [clave[i:i+7] for i in range(len(clave) - 6)]
        for variation in calisto_variations:
            if "calisto".upper() in variation.upper():
                upper_count = sum(1 for c in variation if c.isupper())
                if 2 <= upper_count < 7:
                    return
        raise errores.CalistoError("La clave no contiene la palabra 'calisto' con al menos dos letras mayúsculas pero no todas.")

    def es_valida(self, clave):
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_calisto(clave)
        return True

class Validador:
    def __init__(self, regla):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)