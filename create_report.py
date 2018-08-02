"""Create a report.md that contains specified sections / subsections

Usage: python create_report.py \
        --subsections objection_detection medical\
        --[intersection | union]
"""

import os
import argparse
from collections import defaultdict
import re

import pandas as pd

DOMAIN_OPTIONS = ['medical']
TASK_OPTIONS = [
    'object_classification',
    'object_localization',
    'object_detection',
    'semantic_segmentation',
    'instance_segmentation',
    'image_captioning',
    'cardiac_motion_scoring'
]
TOPIC_OPTIONS = [
    'deep_supervision',
    'efficiency',
    'group_convolutions',
    'loss_functions',
    'non_local_neural_networks',
    'soft_attention',
    'survey_papers'
]

def parse_paper_note_paths(paper_note_paths):
    """Return a DataFrame of titles, filepaths, and paper dates

    :param dict paper_note_paths: holds mapping of paper titles to filepaths
    :return: pd.DataFrame with columns
    - str title: paper title
    - str filepath: relative filepath to paper notes
    - pd.datetime date: date of paper submission
    """

    rows = []
    for paper_title, fpath_paper_notes in paper_note_paths.items():
        with open(fpath_paper_notes, 'r') as f:
            notes = f.read()

        date_matches = re.findall('Date:\ *.*', notes)
        assert len(date_matches) == 1
        # 'Date: 12/21/2013' => '12/21/2013'
        date_str = date_matches[0].split(' ')[1]
        date = pd.to_datetime(date_str, format='%m/%d/%Y')

        rows.append({
            'title': paper_title,
            'fpath_paper_notes': fpath_paper_notes,
            'date': date
        })

    df_paper_note_paths = pd.DataFrame(rows)
    df_paper_note_paths.sort_values('date', inplace=True)
    return df_paper_note_paths

def parse_subsection_papers(subsection, readme_text, paper_note_paths):
    """Parse the papers in the provided subsection

    :param str subsection: name of the subsection
    :param str readme_text: README.md text
    :param dict paper_note_paths: dict of paper titles mapped to filepaths
    :return: updated paper_note_paths dict
    """

    subsection_header = '## {}'.format(
        ' '.join(subsection.split('_')).title()
    )
    
    # Finds all papers under a given subsection header (which spans from one ##
    # to another ##)
    re_to_find = '(?<={}\n)[\s\S]+?(?=\n\n##)'.format(subsection_header)
    matches = re.findall(re_to_find, readme_text)
    assert len(matches) == 1
    match = matches[0].strip()
    paper_texts = match.split('\n')

    for paper_text in paper_texts:
        if not paper_text or paper_text.startswith('#'):
            continue
        # Finds # [paper_title](relative_path) => paper_title
        paper_title_matches = (
            re.findall('(?<=\[)[\s\S]+?(?=\])', paper_text)
        )
        assert len(paper_title_matches) == 1
        paper_title = paper_title_matches[0]
        
        # Finds # [paper_title](relative_path) => relative_path
        paper_relative_path_matches = (
            re.findall('(?<=\()[\s\S]+?(?=\))', paper_text)
        )
        assert len(paper_relative_path_matches) == 1
        paper_relative_path = paper_relative_path_matches[0]
        paper_note_paths[paper_title] = paper_relative_path

    return paper_note_paths


def update_paper_titles(subsection_paths, current_paper_titles,
                        combination_method):
    """Update paper_titles given the combination_method

    :param dict subsection_paths: dict of paper titles mapped to filepaths
    :param set current_paper_titles: set of paper_titles
    :para str combination_method: how to update the paper_titles with the
     subsection_paths; one of ['intersection', 'union', or 'exclusion']
    """

    new_paper_titles = set(subsection_paths)

    if not current_paper_titles:
        current_paper_titles = new_paper_titles
        return current_paper_titles

    if combination_method == 'intersection':
        current_paper_titles = (
            current_paper_titles.intersection(new_paper_titles)
        )
    elif combination_method == 'union':
        current_paper_titles = current_paper_titles.union(new_paper_titles)
    else:
        for new_paper_title in new_paper_titles:
            current_paper_titles.discard(new_paper_title)

    return current_paper_titles


def write_report(df_paper_note_paths, paper_titles):
    """Write the report with the specificied papers"""

    idx_keep = df_paper_note_paths['title'].isin(paper_titles)
    df_paper_note_paths = df_paper_note_paths[idx_keep]
    df_paper_note_paths.sort_values('date', inplace=True)
    
    paper_dicts = (
        df_paper_note_paths[['fpath_paper_notes', 'title']].to_dict('records')
    )
    
    markdown_text = ''
    for paper_dict in paper_dicts:
        with open(paper_dict['fpath_paper_notes'], 'r') as f:
            paper_notes_text = f.read()

        dirname_paper_notes = os.path.dirname(paper_dict['fpath_paper_notes'])
        dirname_paper_notes += '/images'
        paper_notes_text = re.sub(
            './images', dirname_paper_notes, paper_notes_text
        )
        markdown_text += paper_notes_text
        markdown_text += '\n' * 2

    with open('report.md', 'w+') as f:
        f.write(markdown_text)


def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--subsections', type=str, nargs='+',
        help='Subsections to include in the report.md'
    )
    parser.add_argument(
        '--combination_method', type=str,
        choices=['exclusion', 'intersection', 'union'],
        help=(
            'How to combine papers from different sections. For exclusion, '
            'any papers in the first subsection specified are removed if they '
            'are in subsequently specified subsections.'
        )
    )

    args = parser.parse_args()
    return args


def main():
    """Main logic"""

    args = parse_args()

    with open('README.md', 'r') as f:
        readme_text = f.read()
    
    options = set(DOMAIN_OPTIONS)
    options.update(set(TASK_OPTIONS))
    options.update(set(TOPIC_OPTIONS))

    paper_note_paths = {}
    paper_titles = set()
    for subsection in args.subsections:
        subsection_paths = dict()

        msg = ('subsection {} is not one of the possible subsections. '
               'Possible options include {}.'.format(subsection, options))
        assert subsection in options, msg

        subsection_paths = parse_subsection_papers(
            subsection, readme_text, subsection_paths
        )
        paper_titles = update_paper_titles(
            subsection_paths, paper_titles, args.combination_method
        )
        paper_note_paths.update(subsection_paths)
    
    df_paper_note_paths = parse_paper_note_paths(paper_note_paths)
    write_report(df_paper_note_paths, paper_titles)


if __name__ == '__main__':
    main()
