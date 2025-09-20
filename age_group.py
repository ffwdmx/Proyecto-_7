def get_age_group(age):
    """
    Devuelve el grupo de edad basado en la edad en años dentro del intervalo 0..150
    de lo contrario, devuelve 'desconocido'.
    """
    if 0 <= age <= 14:
        return 'infancia'
    elif 15 <= age <= 24:
        return 'juventud'
    elif 25 <= age <= 64:
        return 'adulto'
    elif 65 <= age <= 149:
        return 'vejez'
    else:
        return 'desconocido'


def test_get_age_group():
    """Prueba unitaria para get_age_group"""
    assert get_age_group(-1) == 'desconocido'
    assert get_age_group(0) == 'infancia'
    assert get_age_group(14) == 'infancia'
    assert get_age_group(15) == 'juventud'
    assert get_age_group(24) == 'juventud'
    assert get_age_group(25) == 'adulto'
    assert get_age_group(64) == 'adulto'
    assert get_age_group(65) == 'vejez'
    assert get_age_group(80) == 'vejez'
    assert get_age_group(150) == 'desconocido'


# Ejecutar las pruebas
if __name__ == '__main__':
    try:
        test_get_age_group()
        print("✅ Todas las pruebas pasaron exitosamente!")
        
        # Mostrar ejemplos de uso
        print("\n--- Ejemplos de uso ---")
        test_ages = [-5, 0, 7, 14, 15, 20, 24, 25, 45, 64, 65, 80, 100, 150, 200]
        
        for test_age in test_ages:
            group = get_age_group(test_age)
            print(f"Edad {test_age:3d}: {group}")
            
        # Mostrar rangos de edad
        print("\n--- Rangos de edad definidos ---")
        print("• Infancia: 0-14 años")
        print("• Juventud: 15-24 años") 
        print("• Adulto: 25-64 años")
        print("• Vejez: 65-149 años")
        print("• Desconocido: < 0 o >= 150 años")
        
    except AssertionError as e:
        print(f"❌ Error en las pruebas: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")