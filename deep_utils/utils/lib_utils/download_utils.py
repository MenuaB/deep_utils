import os
import sys
from functools import wraps
import requests


def get_file(fname,
             origin,
             cache_dir=None):
    base_dir, fname = os.path.split(fname)

    if cache_dir is None:
        if 'DEEP_UTILS_HOME' in os.environ:
            cache_dir = os.environ.get('DEEP_UTILS_HOME')
        else:
            cache_dir = os.path.join(os.path.expanduser('~'), '.deep_utils')

    datadir_base = os.path.expanduser(cache_dir)
    datadir = os.path.join(datadir_base, base_dir)
    os.makedirs(datadir, exist_ok=True)

    fpath = os.path.join(datadir, fname)
    if fpath.endswith(".zip"):
        check_path = fpath[:-4]
    else:
        check_path = fpath
    download = False if os.path.exists(check_path) else True

    if download:
        print('Downloading data from', origin)
        error_msg = 'URL fetch failure on {}'
        try:
            with open(fpath, 'wb') as f:
                response = requests.get(origin, stream=True)
                total = response.headers.get('content-length')

                if total is None:
                    f.write(response.content)
                else:
                    downloaded = 0
                    total = int(total)
                    for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                        downloaded += len(data)
                        f.write(data)
                        done = int(50 * downloaded / total)
                        sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                        sys.stdout.flush()
            sys.stdout.write('\n')
        except (Exception, KeyboardInterrupt):
            if os.path.exists(fpath):
                os.remove(fpath)
            raise Exception(error_msg.format(origin))
        if fpath.endswith(".zip"):
            from zipfile import ZipFile
            try:
                with ZipFile(fpath, 'r') as zip:
                    zip.printdir()
                    print(f'extracting {fpath}')
                    zip.extractall(fpath[:-4])
                    print(f'extracting is done!')
                os.remove(fpath)
            except (Exception, KeyboardInterrupt):
                raise Exception(f"Error in extracting {fpath}")
    if fpath.endswith('.zip'):
        fpath = fpath[:-4]
    return fpath


def download_file(url, file_path, unzip=False, remove_zip=False):
    if os.path.isdir(file_path):
        file_name = 'tmp'
        base_dir = file_path
    else:
        base_dir, file_name = os.path.split(file_path)
    os.makedirs(base_dir, exist_ok=True)
    download_des = os.path.join(base_dir, file_name)
    print('Downloading data from', url)
    error_msg = 'URL fetch failure on {}'

    try:
        with open(download_des, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')
    except (Exception, KeyboardInterrupt):
        if os.path.isfile(download_des):
            os.remove(download_des)
        raise Exception(error_msg.format(url))
    if unzip:
        from zipfile import ZipFile
        with ZipFile(download_des, 'r') as zip:
            print(f'extracting {download_des}')
            zip.extractall(base_dir)
            print(f'extracting is done!')
        if remove_zip:
            os.remove(download_des)


def download_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        config = self.config
        download_variables = self.download_variables
        for var in download_variables:
            if getattr(config, var) is None:
                url = getattr(config, var + '_url')
                f_name = getattr(config, var + '_cache')
                f_path = get_file(f_name, url)
                setattr(config, var, f_path)
        return func(self, *args, **kwargs)

    return wrapper


if __name__ == '__main__':
    url = 'https://github.com/Practical-AI/deep_utils/archive/refs/tags/0.4.0.zip'
    download_file(url, '/home/ai', unzip=True, remove_zip=True)
