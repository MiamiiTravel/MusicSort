import click
import eyed3
import os
import shutil

# /Users/isv/dev/music
@click.command()
@click.option('-s', '--src-dir', default='.', help='Source directory.', show_default=True)
@click.option('-d', '--dst-dir', default='.', help='Destination directory.', show_default=True)
def music_sort(src_dir, dst_dir):
    """Simple program that sorts music"""
    while True:
        if os.path.isdir(src_dir):
            # Check access to the source directory
            try:
                # Get iterator
                it = os.scandir(src_dir)
            except PermissionError as e:
                print(str(e))
                print('Please input path to the another source directory. Input q to exit')
                src_dir = input('>>> ')
                if src_dir == 'q':
                    break
            else:
                with it:
                    # Scan all files in the source directory
                    for entry in it:
                        if not entry.name.startswith('.') and entry.is_file() \
                                and entry.name.lower().endswith('.mp3'):

                            # Try to parse ID3 tags
                            try:
                                audiofile = eyed3.load(entry)
                                # Get title
                                if not audiofile.tag.title:
                                    title = entry.name
                                else:
                                    title = audiofile.tag.title.replace('/', ':')
                                # Get artist and album if possible
                                if not audiofile.tag.artist or not audiofile.tag.album:
                                    print(f'Not enough tags to sort file: {entry.name}')
                                    continue
                                else:
                                    # ac/dc -_-
                                    artist = audiofile.tag.artist.replace('/', ':')
                                    album = audiofile.tag.album.replace('/', ':')

                                audiofile.tag.save()
                            except AttributeError as e:
                                print(f'Something wrong with file: {entry.name}')
                            except PermissionError as e:
                                print(f'Have no right to change file: {entry.name}')
                                continue
                            # If file is ok, try to move file
                            else:
                                new_file_name = f'{title} - {artist} - {album}.mp3'
                                # If path exists, then move file
                                if os.path.exists(os.path.join(dst_dir, artist, album)):
                                    shutil.move(os.path.join(src_dir, entry.name),
                                                os.path.join(dst_dir, artist, album, new_file_name))

                                else:
                                    # Try to create new folders for sorted files
                                    try:
                                        os.makedirs(os.path.join(dst_dir, artist, album))
                                    except PermissionError as e:
                                        print(str(e))
                                        print('Please input path to the another destination directory. Input q to exit.')
                                        dst_dir = input('>>> ')
                                        if dst_dir == 'q':
                                            break
                                    # Move file
                                    else:
                                        shutil.move(os.path.join(src_dir, entry.name),
                                                    os.path.join(dst_dir, artist, album, new_file_name))
                                print(f'{os.path.join(src_dir, entry.name)} '
                                      f'-> {os.path.join(dst_dir, artist, album, new_file_name)}')
                # Finish program
                print('Done.')
                break
        # Source directory not found
        else:
            print('Source directory not found.')
            print('Please input path to the existing directory. Input q to exit.')
            src_dir = input('>>> ')
            if src_dir == 'q':
                break


if __name__ == '__main__':
    music_sort()
