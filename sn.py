import vkutils
import mrutils
import mrutils as okutils
# import okutils

def Site(settings):
    if settings.getSite() == 'mr':
        return mrutils.MR(settings)
    if settings.getSite() == 'ok':
        return okutils.OK(settings)
    else:
        return vkutils.VK(settings)
