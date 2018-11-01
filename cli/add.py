# -*- coding: utf-8 -*-
import logging
import click

LOG = logging.getLogger(__name__)


@click.command('baitset', short_help='Load a baitset-file')
@click.argument('path',
    type=click.Path(exists=True),
    required=False
)

@click.option('-i', '--panelid',
    help="The panel identifier name",
)
@click.option('-d', '--date',
    help='date of baitset on format 2017-12-24, default is today.'
)
@click.option('-v', '--version',type=float,)

@click.option('-g', '--genomicbuild',
    help="Genomic build that the baitset is based on, for example hg19"
)
@click.option('-u' '--user',
    help="User that added the baitset"
)
@click.pass_context
def panel(context, panelid, date, version, path, genomicbuild):
    """Add a baitset to the database."""

    adapter = context.obj['adapter']       #Check this up for our adapter

    if not path:
        LOG.warning("Please provide a bait set file (bed-file)")
        context.abort()

    if omim:
        api_key = api_key or context.obj.get('omim_api_key')
        if not api_key:
            LOG.warning("Please provide a omim api key to load the omim gene panel")
            context.abort()
        #Check if OMIM-AUTO exists
        if adapter.gene_panel(panel_id='OMIM-AUTO'):
            LOG.warning("OMIM-AUTO already exists in database")
            LOG.info("To create a new version use scout update omim")
            return

        # Here we know that there is no panel loaded
        try:
            adapter.load_omim_panel(api_key, institute=institute)
        except Exception as err:
            LOG.error(err)
            context.abort()

        return

    panel_lines = get_file_handle(path)

    try:
        panel_info = get_panel_info(
            panel_lines=panel_lines,
            panel_id=panel_id,
            institute=institute,
            version=version,
            date=date,
            display_name=display_name
            )
    except Exception as err:
        LOG.warning(err)
        context.abort()

    version = None
    if panel_info.get('version'):
        version = float(panel_info['version'])

    panel_id = panel_info['panel_id']
    display_name = panel_info['display_name'] or panel_id
    institute = panel_info['institute']
    date = panel_info['date']

    if not institute:
        LOG.warning("A Panel has to belong to a institute")
        context.abort()

    #Check if institute exists in database
    if not adapter.institute(institute):
        LOG.warning("Institute {0} does not exist in database".format(institute))
        context.abort()

    if not panel_id:
        LOG.warning("A Panel has to have a panel id")
        context.abort()

    if version:
        existing_panel = adapter.gene_panel(panel_id, version)
    else:
        existing_panel = adapter.gene_panel(panel_id)
        ## Assuming version 1.0
        version = 1.0

    if existing_panel:
        LOG.info("found existing panel")
        if version == existing_panel['version']:
            LOG.warning("Panel with same version exists in database")
            LOG.info("Reload with updated version")
            context.abort()
        display_name = display_name or existing_panel['display_name']
        institute = institute or existing_panel['institute']

    try:
        adapter.load_panel(
            path=path,
            institute=institute,
            panel_id=panel_id,
            date=date,
            panel_type=panel_type,
            version=version,
            display_name=display_name
        )
    except Exception as err:
        LOG.warning(err)
        context.abort()