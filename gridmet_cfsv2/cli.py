import datetime

import click
import numpy as np
import sys


def yesterday():
    return datetime.date.isoformat(datetime.date.today() - datetime.timedelta(days=1))


def validate_date(date_string):
    try:
        date = datetime.date.fromisoformat(date_string)
    except ValueError:
        raise click.BadParameter("not an ISO formatted date ({0})".format(date_string))
    else:
        return date


@click.command()
@click.option(
    '-q',
    '--quiet',
    is_flag=True,
    help=(
        'Don\'t emit non-error messages to stderr. Errors are still emitted, '
        'silence those with 2>/dev/null.'
    ),
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Also emit status messages to stderr."
)
@click.option(
    '--start',
    metavar='YYYY-MM-DD',
    default=yesterday,
    help='Start date',
    show_default='yesterday',
)
@click.option(
    '--end',
    metavar='YYYY-MM-DD',
    default=yesterday,
    help='End date',
    show_default='yesterday',
)
@click.option(
    "--hrumap",
    is_flag=True,
    help='map gridmet to HRUs'
)
@click.option(
    '--hru_ids',
    default=np.empty(shape=(1), dtype=int),
    help='HRU ids as 1-d numpy array of int',
)
@click.option(
    '--wght_file',
    type=click.Path(exists=True),
    metavar='path_to_file.csv',
    help='weights file',
)
@click.option(
    '--config_file',
    type=click.Path(exists=True),
    metavar='path_to_file.yaml',
    help='config file'
)
# def touch(whgt_file):
#     click.echo(click.format_filename(whgt_file))
@click.argument("var", type=click.Choice(["tmin", "tmax", "precip"]))
def main(quiet, verbose, config_file, start, end, var, hrumap, hru_ids, wght_file):
    print('test')
    # fetcher = Gridmet(start, end_date=end, hrumap=hrumap, hru_id=hru_ids, wght_file=wght_file)
    # fetcher = Gridmet(config_file=config_file)
    # print(getattr(fetcher, var))


if __name__ == "__main__":
    sys.exit(main())
