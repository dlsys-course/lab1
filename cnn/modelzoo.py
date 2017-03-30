import os

_base_model_url = 'http://data.mxnet.io/models/'
_default_model_info = {
    'imagenet1k-inception-bn': {'symbol':_base_model_url+'imagenet/inception-bn/Inception-BN-symbol.json',
                             'params':_base_model_url+'imagenet/inception-bn/Inception-BN-0126.params'},
    'imagenet1k-resnet-18': {'symbol':_base_model_url+'imagenet/resnet/18-layers/resnet-18-symbol.json',
                             'params':_base_model_url+'imagenet/resnet/18-layers/resnet-18-0000.params'},
    'imagenet1k-resnet-34': {'symbol':_base_model_url+'imagenet/resnet/34-layers/resnet-34-symbol.json',
                             'params':_base_model_url+'imagenet/resnet/34-layers/resnet-34-0000.params'},
    'imagenet1k-resnet-50': {'symbol':_base_model_url+'imagenet/resnet/50-layers/resnet-50-symbol.json',
                             'params':_base_model_url+'imagenet/resnet/50-layers/resnet-50-0000.params'},
    'imagenet1k-resnet-101': {'symbol':_base_model_url+'imagenet/resnet/101-layers/resnet-101-symbol.json',
                             'params':_base_model_url+'imagenet/resnet/101-layers/resnet-101-0000.params'},
    'imagenet1k-resnet-152': {'symbol':_base_model_url+'imagenet/resnet/152-layers/resnet-152-symbol.json',
                             'params':_base_model_url+'imagenet/resnet/152-layers/resnet-152-0000.params'},
    'imagenet1k-resnext-50': {'symbol':_base_model_url+'imagenet/resnext/50-layers/resnext-50-symbol.json',
                             'params':_base_model_url+'imagenet/resnext/50-layers/resnext-50-0000.params'},
    'imagenet1k-resnext-101': {'symbol':_base_model_url+'imagenet/resnext/101-layers/resnext-101-symbol.json',
                             'params':_base_model_url+'imagenet/resnext/101-layers/resnext-101-0000.params'},
    'imagenet11k-resnet-152': {'symbol':_base_model_url+'imagenet-11k/resnet-152/resnet-152-symbol.json',
                             'params':_base_model_url+'imagenet-11k/resnet-152/resnet-152-0000.params'},
    'imagenet11k-place365ch-resnet-152': {'symbol':_base_model_url+'imagenet-11k-place365-ch/resnet-152-symbol.json',
                                          'params':_base_model_url+'imagenet-11k-place365-ch/resnet-152-0000.params'},
    'imagenet11k-place365ch-resnet-50': {'symbol':_base_model_url+'imagenet-11k-place365-ch/resnet-50-symbol.json',
                                         'params':_base_model_url+'imagenet-11k-place365-ch/resnet-50-0000.params'},
}


def download_file(url, local_fname=None, force_write=False):
    # requests is not default installed
    import requests
    if local_fname is None:
        local_fname = url.split('/')[-1]
    if not force_write and os.path.exists(local_fname):
        return local_fname

    dir_name = os.path.dirname(local_fname)

    if dir_name != "":
        if not os.path.exists(dir_name):
            try: # try to create the directory if it doesn't exists
                os.makedirs(dir_name)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    r = requests.get(url, stream=True)
    assert r.status_code == 200, "failed to open %s" % url
    with open(local_fname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_fname

def download_model(model_name, dst_dir='./', meta_info=None):
    if meta_info is None:
        meta_info = _default_model_info
    meta_info = dict(meta_info)
    if model_name not in meta_info:
        return (None, 0)
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)
    meta = dict(meta_info[model_name])
    assert 'symbol' in meta, "missing symbol url"
    model_name = os.path.join(dst_dir, model_name)
    download_file(meta['symbol'], model_name+'-symbol.json')
    assert 'params' in meta, "mssing parameter file url"
    download_file(meta['params'], model_name+'-0000.params')
    return (model_name, 0)
