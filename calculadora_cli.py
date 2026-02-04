"""Calculadora CLI - Interfaz de línea de comando"""

import argparse
import sys
from rich.console import Console

console = Console()

from calculadora_completa import (
    estadistica_descriptiva_from_list,
    main as calculadora_main,
)


def parse_data(s: str):
    """Parsear datos separados por comas"""
    parts = [x.strip() for x in s.split(',') if x.strip()]
    return [float(x) for x in parts]


def cmd_stats(args):
    """Calcular estadísticas desde datos manuales"""
    if args.data:
        numbers = parse_data(args.data)
        estadistica_descriptiva_from_list(numbers)
    else:
        console.print("[red]Error: se requiere --data para esta acción[/red]")


def cmd_interactive(args):
    """Abre la interfaz interactiva"""
    calculadora_main()


def main():
    parser = argparse.ArgumentParser(prog='CalculadoraCLI')
    sub = parser.add_subparsers(dest='command')

    sub_stats = sub.add_parser('stats', help='Calcula estadísticas desde datos manuales')
    sub_stats.add_argument('--data', '-d', help='Datos separados por comas, ej: "1,2,3,4"')
    sub_stats.set_defaults(func=cmd_stats)

    sub_inter = sub.add_parser('interactive', help='Abre la interfaz interactiva')
    sub_inter.set_defaults(func=cmd_interactive)

    args = parser.parse_args()
    if not args.command:
        cmd_interactive(args)
        return

    args.func(args)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        print("\n[ERROR] Ha ocurrido un error inesperado:\n")
        traceback.print_exc()
        print("\nPresiona ENTER para salir...")
        input()
