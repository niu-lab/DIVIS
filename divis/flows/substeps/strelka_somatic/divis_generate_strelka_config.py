import click

tpl = '''

[user]

isSkipDepthFilters = {is_wes}

maxInputDepth = 10000

depthFilterMultiple = 3.0

snvMaxFilteredBasecallFrac = 0.4

snvMaxSpanningDeletionFrac = 0.75

indelMaxRefRepeat = 8

indelMaxWindowFilteredBasecallFrac = 0.3

indelMaxIntHpolLength = 14

ssnvPrior = 0.000001
sindelPrior = 0.000001

ssnvNoise = 0.0000005
sindelNoise = 0.000001

ssnvNoiseStrandBiasFrac = 0.5

minTier1Mapq = 20

minTier2Mapq = 5

ssnvQuality_LowerBound = 15

sindelQuality_LowerBound = 30

isWriteRealignedBam = 0

binSize = 25000000

extraStrelkaArguments =

'''


@click.command()
@click.option('--wes', required=True, type=bool, help="is wes or not")
def gen_config(wes):
    if wes:
        config = tpl.format(is_wes=1)
    else:
        config = tpl.format(is_wes=0)
    with open("strelka_config_bwa_default.ini", "w+") as file:
        file.write(config)


if __name__ == "__main__":
    gen_config()
