import WordsGenerator as wg

def Main():
    shape = (3, 1)
    shape = wg.CheckShape(shape)
    objs = wg.ReadObjs(shape, 3)
    for i, obj in enumerate(objs):
        im = wg.DrawGrid(shape)
        tilesDist, err = wg.ChooseTiles(shape, len(obj))
        wg.ScatterObjects(obj, tilesDist, im)

        im.show()
        im.save(r'imgs\{}.png'.format(format(i, "03")) )

if __name__ == '__main__':
    Main()