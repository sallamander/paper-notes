"""Create the main README.md

This cycles through each of the directories in the repository and creates three
sections for the README.md:

    1.) Papers organized by task (e.g. object detection, semantic segmentation,
        etc.).
    2.) Papers organized by domain (e.g. medical)
    3.) Papers organized by topic (e.g. deep supervision, non-local networks,
        attention, etc.).
"""

import os
import re
from collections import defaultdict

import pandas as pd

DOMAIN_OPTIONS = ['medical']
TASK_OPTIONS = [
    'action_classification',
    'object_classification',
    'object_localization',
    'object_detection',
    'scene_classification',
    'semantic_segmentation',
    'instance_segmentation',
    'image_captioning',
    'image_registration',
    'pose_estimation',
    'cardiac_motion_scoring'
]
TOPIC_OPTIONS = [
    'deep_supervision',
    'efficiency',
    'group_convolutions',
    'loss_functions',
    'non_local_neural_networks',
    'post_processing',
    'soft_attention',
    'survey_papers',
    'weak_supervision',
    'unsupervised_learning'
]


def create_main_readme(sections_dict):
    """Create the main README.md file from the data in df_markdown_files

    The main README will have three sections - one where papers are organized
    by domain, one by task, and one by topic. Within each section, papers will
    be organized by date. This function parses the infromation from
    df_markdown_files (where each row 

    :param dict sections_dict: dict of dicts holding section information
    :return: str holding the README text
    """

    readme_text = ''

    doctoc_start = (
        '<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n'
        '<!-- DON\'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n'
        '**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*\n'
    )
    doctoc_end = (
        '<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n'
    )

    readme_text += doctoc_start
    readme_text += doctoc_end
    readme_text += ('\n' * 2)

    for section in ('tasks', 'domains', 'topics'):
        section_header = 'Papers organized by {}'.format(section[:-1]).title()
        section_header = '# {}'.format(section_header)
        readme_text += section_header
        readme_text += ('\n' * 2)
        
        if section == 'domains':
            options = DOMAIN_OPTIONS
        elif section == 'tasks':
            options = TASK_OPTIONS
        elif section == 'topics':
            options = TOPIC_OPTIONS
        
        for subsection in options:
            subsection_title = '## {}'.format(
                ' '.join(subsection.split('_')).title()
            )
            readme_text += subsection_title
            readme_text += '\n'

            for paper_title in sections_dict[section][subsection]:
                readme_text += paper_title
                readme_text += '  \r\n'
            
            # Skip the extra line for the last topic in the README
            if not subsection == TOPIC_OPTIONS[-1]:
                readme_text += '\n'
        if not section == 'topics':
            readme_text += ('\n' * 2)

    with open('README.md', 'w+') as f:
        f.write(readme_text)


def get_markdown_filepaths():
    """Return a list of Markdown filepaths

    :return: list[str] holding filepaths to Markdown files
    """

    dirpath_current = os.getcwd()

    fpaths_markdown = []
    for dirpath, dirnames, fnames in os.walk(dirpath_current):
        for fname in fnames:
            if fname.endswith('.md'):
                fpath = os.path.join(dirpath, fname)
                fpaths_markdown.append(fpath)
    
    return fpaths_markdown


def parse_df_markdown_files(df_markdown_files):
    """Parse the df_markdown_files into sections for the README

    :param pd.DataFrame df_markdown_files: each row contains information for a
     single markdown file, and columns include fpath_markdown, date,
     domains, tasks, and topics
    :return: dict of dicts holding section information
    """

    dirpath_current = os.getcwd()
    sections_dict = defaultdict(dict)

    for _, row in df_markdown_files.iterrows():
        fpath_markdown_absolute = row['fpath_markdown']
        fpath_markdown_relative = fpath_markdown_absolute.replace(
            dirpath_current, '.'
        )
        
        with open(fpath_markdown_absolute, 'r') as f:
            line0 = next(f)

            opening_bracket = line0.find("[")
            closing_bracket = line0.find("]")
            title = line0[opening_bracket:closing_bracket + 1]

            readme_line = title + "({})".format(fpath_markdown_relative)

        for section in ('domains', 'tasks', 'topics'):
            for section_tag in row[section]:
                if section_tag not in sections_dict[section]:
                    sections_dict[section][section_tag] = []
                sections_dict[section][section_tag].append(readme_line)

    return sections_dict

def parse_markdown_files(fpaths_markdown):
    """Parse markdown files for metadata

    Metadata includes the date of submission (labeled as "Date" in the note
    files) as well as the paper task(s) (labeled as task.[task_name]), topic(s)
    (labeled as topic.[topic_name]), and paper domain(s) (labeled as
    domain.[domain_name]).

    :param list[str] fpaths_markdown: filepaths to the Markdown files to parse
    :return: pd.DataFrame with columns:
    - str fpath_markdown: filepath to a Markdown file
    - pd.datetime date: date stored in the Markdown file
    - list[str] domains: domains stored in the Markdown file
    - list[str] tasks: tasks stored in the Markdown file
    - list[str] topics: topics stored in the Markdown file
    """

    rows = []
    for fpath_markdown in fpaths_markdown:
        domains, tasks, topics = [], [], []
        with open(fpath_markdown, 'r') as f:
            notes = f.read()

            date_matches = re.findall('Date:\ *.*', notes)
            assert len(date_matches) == 1
            # 'Date: 12/21/2013' => '12/21/2013'
            date_str = date_matches[0].split(' ')[1]
            date = pd.to_datetime(date_str, format='%m/%d/%Y')

            tag_matches = re.findall('Tags:\ *.*', notes)
            assert len(tag_matches) == 1
            tags_str = tag_matches[0]
            tags_str = tags_str.replace('Tags:\ ', '')

            tags = tags_str.split(',')
            for tag in tags:
                if 'domain' in tag:
                    domains.append(tag.split('domain.')[1].strip())
                if 'task' in tag:
                    tasks.append(tag.split('task.')[1].strip())
                elif 'topic' in tag:
                    topics.append(tag.split('topic.')[1].strip())

            assert len(tasks) >= 1
            
            rows.append({
                'fpath_markdown': fpath_markdown,
                'date': date,
                'domains': domains,
                'tasks': tasks,
                'topics': topics
            })

    df_markdown_files = pd.DataFrame(rows)
    df_markdown_files.sort_values('date', inplace=True)
    return df_markdown_files


def main():
    """Main logic"""

    fpaths_markdown = get_markdown_filepaths()
    df_markdown_files = parse_markdown_files(fpaths_markdown)
    sections_dict = parse_df_markdown_files(df_markdown_files)
    create_main_readme(sections_dict)


if __name__ == '__main__':
    main()
