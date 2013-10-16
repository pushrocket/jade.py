import lib

parser = lib.Parser('div Woah. This actually worked!', 'tag.jade')

print(parser.parse().nodes[0].block.nodes[0].val)