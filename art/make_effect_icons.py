"""18x18 status-effect icons for Apocalypse Pantry (written into the mod resources)."""
import os
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'src', 'main', 'resources', 'assets', 'apocalypsepantry', 'textures', 'mob_effect')
os.makedirs(OUT, exist_ok=True)

def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)

ICONS = {
    # biohazard-like blot: green core with dark spots
    'infection': (['......aaaaaa......',
                   '....aabbbbbbaa....',
                   '...abbccccccbba...',
                   '..abccbbccbbccba..',
                   '..abcbddbbddbcba..',
                   '.abccbddbbddbccba.',
                   '.abccbbbbbbbbccba.',
                   '.abcccbbccbbcccba.',
                   '.abccccbddbccccba.',
                   '.abcccbbddbbcccba.',
                   '.abccbbbbbbbbccba.',
                   '..abccbbccbbccba..',
                   '..abccccccccccba..',
                   '...abbccccccbba...',
                   '....aabbbbbbaa....',
                   '......aaaaaa......',
                   '..................',
                   '..................'],
                  {'a': '#1E2A12', 'b': '#4E7A26', 'c': '#8ED14E', 'd': '#2B3A18'}),
    # a green wisp drifting up
    'undead_scent': (['..................',
                      '.......aa.........',
                      '......abba........',
                      '......abcba.......',
                      '.......abcba......',
                      '........abcba.....',
                      '.......abcba......',
                      '......abcba.......',
                      '.....abcba........',
                      '.....abcba........',
                      '......abcba.......',
                      '.......abcba......',
                      '........abba......',
                      '..aa.....aa...aa..',
                      '.abba.........abba',
                      '.abcba.......abcba',
                      '..aaaa.......aaaa.',
                      '..................'],
                     {'a': '#1E2A12', 'b': '#6B7340', 'c': '#C3EA6C'}),
    # lightning bolt
    'adrenaline': (['..........aaaa....',
                    '.........abbba....',
                    '........abbca.....',
                    '.......abbca......',
                    '......abbca.......',
                    '.....abbcaaaaa....',
                    '....abbccccbba....',
                    '...aaaaabbcba.....',
                    '......abbcba......',
                    '.....abbcba.......',
                    '....abbcba........',
                    '...abbcba.........',
                    '..abbca...........',
                    '..abca............',
                    '..aba.............',
                    '..aa..............',
                    '..................',
                    '..................'],
                   {'a': '#4A2E0C', 'b': '#F5A623', 'c': '#FFF0A0'}),
    # down arrow, washed-out purple
    'crash': (['..................',
               '......aaaaaa......',
               '......abbbba......',
               '......abccba......',
               '......abccba......',
               '......abccba......',
               '......abccba......',
               '..aaaaabccbaaaaa..',
               '..abbbbbccbbbbba..',
               '...abccccccccba...',
               '....abccccccba....',
               '.....abccccba.....',
               '......abccba......',
               '.......abba.......',
               '........aa........',
               '..................',
               '..................',
               '..................'],
              {'a': '#241C34', 'b': '#6A5A8C', 'c': '#B7A6D8'}),
    # drumstick
    'stamina': (['..................',
                 '........aaaa......',
                 '......aabbbbaa....',
                 '.....abbccbbbba...',
                 '....abbcccbbbbba..',
                 '....abccbbbbbbba..',
                 '....abbbbbbbbbba..',
                 '.....abbbbbbbba...',
                 '......abbbbbbba...',
                 '.......aabbbaa....',
                 '........adda......',
                 '.......adda.......',
                 '.....aadda........',
                 '....aeeda.........',
                 '....aeea..........',
                 '.....aa...........',
                 '..................',
                 '..................'],
                {'a': '#3A1A10', 'b': '#C95C2C', 'c': '#F49A47', 'd': '#E2D6B4', 'e': '#F2EAD2'}),
}
for name, (rows, pal) in ICONS.items():
    im = Image.new('RGBA', (18, 18), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 18, (name, y, len(row))
        for x, ch in enumerate(row):
            if ch != '.':
                im.putpixel((x, y), hx(pal[ch]))
    im.save(os.path.join(OUT, name + '.png'))
print('effect icons:', ', '.join(ICONS))
