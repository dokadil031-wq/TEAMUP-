with open("app/src/main/java/com/example/MaidanViewModel.kt", "r") as f:
    text = f.read()

lines = text.split('\n')
while True:
    count = 0
    idx2 = -1
    for i, l in enumerate(lines):
        if "private fun listenToMatches()" in l:
            count += 1
            if count == 2:
                idx2 = i
                break
    
    if idx2 == -1:
        break
        
    b = 0
    end2 = -1
    for i in range(idx2, len(lines)):
        b += lines[i].count('{')
        b -= lines[i].count('}')
        if '{' in lines[idx2] or any('{' in l for l in lines[idx2:i+1]):
            if b == 0:
                end2 = i
                break
                
    if end2 != -1:
        print(f"Deleting {idx2} to {end2}")
        del lines[idx2:end2+1]
    else:
        break

with open("app/src/main/java/com/example/MaidanViewModel.kt", "w") as f:
    f.write('\n'.join(lines))
