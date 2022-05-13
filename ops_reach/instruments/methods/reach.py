# -*- coding: utf-8 -*-
"""Provides metadata specific routines for REACH data."""

import datetime as dt


ackn_str = ' '.join(('The development of the CDF files was supported by the SPI',
                     'Goddard HISFM 2022. The success of the REACH project is',
                     'owed to a long line of people who have contributed to it',
                     'over the many years of development. The REACH hardware',
                     'team in The Aerospace Corporation’s xLab organization',
                     'included Paul Carranza, Sue Crain, Bill Crain, Andrew Hsu,',
                     'Brian McCarthy, John McHale, Can Nguyen, Mario Perez, Deb',
                     'Salvaggio, and Gerrit Sorensen, all critical to designing',
                     'and fabricating the first 18 of the 32 REACH pods. Millennium',
                     'Engineering and Integration (MEI) manufactured the remaining',
                     '14 pods. Doug Holker was instrumental in nearly all facets of',
                     'REACH development, outreach, support, endorsement and project',
                     'management for the entirety of the project’s lifetime. The',
                     'REACH project was led in chronological order by the following',
                     'USAF Program Managers: Capt Dan Kimmich, Lt Garrett Ellis, Lt',
                     'Justin Shimasaki, Capt Sean Quintana, Capt Felix Abeyta, Lt',
                     'Kurt Mann, Maj James Crane, Capt Omar Manning, Lt Zach Morley,',
                     'Capt Scott Day, Lt Zeesha Braslawsce, and Lt Ryan Francies. This',
                     'list reflects their ranks at the time of involvement. Recent',
                     'management is possible through the SMC/Development Corp program',
                     'office support Pete Cunningham. Data transport is provided by',
                     'Iridium, L3Harris, and data processing of the Level 0 files is',
                     'performed by Robin Barnes and supported by Tom Sotirelis and',
                     'Mike Kelly at the Johns Hopkins Applied Physics Laboratory.',
                     'Alexa Halford, now of NASA Goddard Space Flight Center,',
                     'prototyped many higher-level REACH data products and performed',
                     'intra-calibration of the dosimeters.'))


def generate_header(inst_id, epoch):
    """Generate the meta header info.

    Parameters
    ----------
    inst_id : str
        The VID of the associated dataset.
    epoch : dt.datetime
        The epoch of the datafile.  Corresponds to the first data point.

    Returns
    -------
    header : dict
        A dictionary compatible with teh pysat.meta_header format.  Top-level
        metadata for the file.

    """

    header = {'Project': 'The Aerospace Corporation',
              'Discipline': 'Space Physics>Magnetospheric Science, Space Weather',
              'Data_type': 'pre>Preliminary',
              'Descriptor': ' '.join(('reach-v3', inst_id, '>, The Responsive',
                                      'Environmental Assessment Commercially',
                                      'Hosted (REACH)  version-3 Data for,'
                                      'vehical ID ', inst_id)),
              'TITLE': 'Responsive Environmental Assessment Commercially Hosted',
              'TEXT': ' '.join(('The Responsive Environmental Assessment Commercially',
                                'Hosted (REACH) constellation is collection of 32 small',
                                'sensors hosted on six orbital planes of the',
                                'Iridium-Next space vehicles in low earth orbit.',
                                'Each sensor contains two micro-dosimeters sensitive',
                                'to the passage of charged particles from the Earth’s',
                                'radiation belts. There are six distinct dosimeter',
                                'types spread among the 64 individual sensors, which',
                                'are unique in shielding and electronic threshold. When',
                                'taken together, this effectively enables a high',
                                'time-cadence measurement of protons and electrons in',
                                'six integral energy channels over the entire globe.')),
              'Source_name': ' '.join(('reach>The Responsive Environmental Assessment',
                                       'Commercially Hosted, satellite id ', inst_id)),
              'Logical_source': ''.join(('reach.', epoch.strftime('%Y%m%d'),
                                         '.vid-', inst_id, '.l1b.v3')),
              'File_naming_convention': 'source_date_vehicalID_descriptor',
              'Data_version': '03',
              'Software_version': 'l1b',
              'PI_name': 'Joe Mazu (joseph.e.mazur@aero.or)',
              'PI_affiliation': 'The Aerospace Corporation',
              'Data_Curator': 'Timothy B. Guild (Timothy.B.Guild@aero.org)',
              'DC_afiliation': 'The Aerospace Corporation',
              'Instrument_type': 'Particles (space)',
              'Mission_group': ' '.join(('The Responsive Environmental Assessment',
                                         'Commercially Hosted (REACH)')),
              'Time_resolution': '5 seconds',
              'Rules_of_use': ''.join(('See Usage Guidelines at: https://',
                                       'zenodo.org/record/6423507#.YmMqcfPMLCU')),
              'Generated_by': ' '.join(('csv files generated at The Aerosapce',
                                        'Corporation, CDF files generated by Alexa',
                                        'Halford at NASA Goddard Space Flight Center')),
              'Generation_date': dt.datetime.today().strftime('%Y-%m-%d'),
              'Generation_datetime': dt.datetime.today().isoformat(),
              'Acknowledgement': ackn_str,
              'LINK_TEXT': 'REACH csv files are avalible at ',
              'LINK_TITLE': 'REACH data ',
              'HTTP_LINK': 'https://zenodo.org/record/6423507#.YmMwUfPMLCV'}

    return header
