import sys
import wave

if len(sys.argv) < 2:
    sys.stderr.write("Usage: split_wav.py <options> <filename>\nOptions:\n-mono : Split to mono files\n")
    sys.exit(1)

mono = False

arg = 1
if sys.argv[arg] == '-mono':
	mono = True
	arg += 1
filename = sys.argv[arg]

F = wave.open( filename, 'r' )

channels = F.getnchannels()

width = F.getsampwidth()
frames = F.getnframes()
frame_bytes = channels * width
print ( 'channels %d, sample width %d, frame size %d, frames %d' % ( channels, width, frame_bytes, frames ) )

GG = []
remaining = channels
index = 1
while remaining > 0:
	G = wave.open( filename.replace('.', '.%d.'%index), 'w' )
	if mono or ( remaining == 1 ):
		G.setnchannels( 1 )
	else:
		G.setnchannels( 2 )
	remaining -= G.getnchannels()
	index += 1
	G.setsampwidth( width )
	G.setframerate( F.getframerate() )
	GG.append( G )

for i in range(frames):
	f = F.readframes(1)
	p0 = 0
	for G in GG:
		p1 = p0 + G.getnchannels() * width
		G.writeframesraw( f[p0:p1] )
		p0 = p1

for G in GG:
	G.close()
