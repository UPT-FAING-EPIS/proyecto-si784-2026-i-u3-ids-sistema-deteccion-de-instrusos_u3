Feature: Dashboard de TrafficWatch IDS
  Como equipo del proyecto
  Quiero validar el dashboard desde escenarios BDD
  Para confirmar que las funciones demo siguen disponibles en CI

  Scenario: Consultar estado del IDS
    Given el dashboard Flask esta disponible
    When consulto la API de estado
    Then recibo un estado valido del IDS

  Scenario: Generar una alerta simulada
    Given el dashboard Flask esta disponible
    When genero una simulacion de fuerza bruta SSH
    Then la alerta queda registrada en el historial
