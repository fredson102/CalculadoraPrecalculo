"""Calculadora CLI
Permite ejecutar funciones desde la línea de comando o abrir la interfaz interactiva.
Ejemplos:
  python calculadora_cli.py demo
  python calculadora_cli.py stats --data "12,7.5,3,9.25,14"
  python calculadora_cli.py stats-image --image sample_numbers.png
  python calculadora_cli.py interactive
"""

import argparse
import sys
from rich.console import Console
from rich.table import Table

console = Console()

from calculadora_completa import (
    resolver_ecuacion_lineal,
    resolver_ecuacion_cuadratica,
    sistema_ecuaciones_lineales,
    funcion_exponencial,
    funcion_logaritmica,
    trigonometria_basica,
    interes_compuesto,
    estadistica_descriptiva_from_list,
    ocr_estadistica,
    find_tesseract,
)

# Helper to parse comma separated list

def parse_data(s: str):
    parts = [x.strip() for x in s.split(',') if x.strip()]
    return [float(x) for x in parts]


def cmd_demo(args):
    # Use demo_ocr if available
    from demo_ocr import run_demo
    run_demo()


def cmd_stats(args):
    if args.data:
        numbers = parse_data(args.data)
        stats = estadistica_descriptiva_from_list(numbers)
        if stats and args.output:
            from calculadora_completa import save_stats_to_csv
            save_stats_to_csv(stats, args.output)
    else:
        console.print("[red]Error: se requiere --data para esta acción[/red]")


def cmd_stats_image(args):
    if args.image:
        if find_tesseract() is None:
            console.print('[red]Tesseract no encontrado. Instala el ejecutable y vuelve a intentarlo.[/red]')
            return
        stats = ocr_estadistica(args.image)
        if stats and args.output:
            from calculadora_completa import save_stats_to_csv
            save_stats_to_csv(stats, args.output)
    else:
        console.print("[red]Error: se requiere --image para esta acción[/red]")


def cmd_interactive(args):
    # Launch existing interactive menu
    from calculadora_completa import main
    main()


def main():
    parser = argparse.ArgumentParser(prog='calculadora_cli')
    sub = parser.add_subparsers(dest='command')

    sub_demo = sub.add_parser('demo', help='Ejecuta demo OCR y estadísticas')
    sub_demo.set_defaults(func=cmd_demo)

    sub_stats = sub.add_parser('stats', help='Calcula estadísticas desde datos manuales')
    sub_stats.add_argument('--data', '-d', help='Datos separados por comas, ej: "1,2,3,4"')
    sub_stats.add_argument('--output', '-o', help='Archivo CSV para guardar resultados (opcional)')
    sub_stats.set_defaults(func=cmd_stats)

    sub_stats_img = sub.add_parser('stats-image', help='Ejecuta OCR sobre imagen y calcula estadísticas')
    sub_stats_img.add_argument('--image', '-i', help='Ruta a la imagen')
    sub_stats_img.add_argument('--output', '-o', help='Archivo CSV para guardar resultados (opcional)')
    sub_stats_img.set_defaults(func=cmd_stats_image)

    sub_inter = sub.add_parser('interactive', help='Abre la interfaz interactiva basada en menú')
    sub_inter.set_defaults(func=cmd_interactive)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
