import os


def fixtures_path(filename):
    return os.path.normpath(os.path.join('tests', 'fixtures', filename))


def output_path(filename):
    return os.path.normpath(os.path.join('tests', 'temp', filename))


def clear_files():
    output_folder = os.path.normpath(os.path.join('tests', 'temp'))
    for file in os.listdir(output_folder):
        if os.path.basename(file) == '.gitkeep':
            continue
        os.remove(os.path.join(output_folder, file))
