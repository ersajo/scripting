#!/usr/bin/python

"""
Para ejecutar el script
py adnMigration.py [routeToSourceFile]
"""

import sys
import re
import json

stack = []
finalArray = []
index = -1
canSave = False
numElem = 1

def addRow(container, itemId):
  if not container: return
  if container.get('type') == 'text': return
  if container.get('id') == itemId:
    global numElem
    if container.get('type') == 'column':
      container.get('content').append({'id': numElem, 'type': 'row', 'name': 'Row', 'canDelete': False, 'content': []})
    if container.get('type') == 'row':
      container.get('content').append({'id': numElem, 'type': 'column', 'size': 'col-lg', 'content': []})
    return
  for row in container.get('content'):
    addRow(row, itemId)

def addText(container, itemId, text):
  if not container: return
  if container.get('type') == 'text': return
  if container.get('id') == itemId:
    global numElem
    if container.get('type') == 'container' and len(container.get('content')) == 0:
      container.get('content').append({'id': numElem, 'type': 'row', 'name': 'Row', 'canDelete': False, 'content': []})
    container = container.get('content')[-1]
    if container.get('type') == 'row' and len(container.get('content')) == 0:
      container.get('content').append({'id': numElem, 'type': 'column', 'size': 'col-lg', 'content': []})
    container = container.get('content')[-1]
    if container.get('type') == 'column':
      container.get('content').append({'type': 'text', 'name': 'Text', 'value': text})
    return
  for row in container.get('content'):
    addText(row, itemId, text)

def getStackId():
  global stack
  for item in reversed(stack):
    if item.get('element') == 'container' or item.get('element') == 'row' or item.get('element') == 'column':
      return item.get('id')

# Open file in read mode
readFile = open(sys.argv[1], 'r', encoding='utf-8')
# Split body into tags from input file
body = readFile.read().split('<body')[1].split('</body>')[0].split('<')
# Delete body open tag
del body[0]
# Close reading file
readFile.close()
indexToDelete = []

# Loop to add < to every tag and one line for tag
for index in range(len(body)):
  body[index] = '<' + body[index]
  body[index] = body[index].replace('\n', ' ')

# Loop to identify useless lines
index = -1
for line in body:
  index += 1
  # Look for scripts tags
  if line.find('<script') != -1:
    start = index
    while body[start].find('</script>') == -1:
      indexToDelete.append(start)
      start += 1
    indexToDelete.append(start)

# Delete lines useless from the array
for index in reversed(indexToDelete):
  del body[index]

# Create an output.html file to see the body
newFile = open('output.html', 'w')
for line in body:
  newFile.write(line + '\n')

# Loop to search containers
index = -1
for line in body:
  index += 1
  
  # Regular expresion to find close tags
  if re.search(r'</.+>', line):
    # Do only if has containers in array
    if len(stack) > 0:
      item = stack.pop()
      if len(stack) == 0: canSave = False
      # Verify if popped item has element attribute
      if item.get('element'):
        if item.get('element') == 'Text':
          textContent = ''
          for itemId in range(item['index'] - 1, index):
            textContent = textContent + body[itemId]
          addText(finalArray[-1], getStackId(), textContent)
  else:
    if re.search(r'msp39_Content"', line):
      # Regular expresion to body
      stack.append({'id': numElem, 'tag': line.strip().split(' ')[0][1:].split('>')[0], 'index': index + 1})
      canSave = True
    elif re.search(r'<br>', line):
      # Skip br tags
      continue
    elif re.search(r'<!--', line):
      # Skip comments
      continue
    elif re.search(r'<input', line):
      # Skip input tags
      continue
    else:
      # Append tags to stack
      if canSave and len(stack) == 0:
        break
      elif re.search(r'&nbsp;', line):
        # Skip empty containers
        stack.append({'id': numElem, 'tag': line.strip().split(' ')[0][1:], 'index': index + 1, 'element': 'emptyTag'})
        numElem += 1
      elif len(stack) == 1 and canSave:
        # Add every container in first level
        stack.append({'id': numElem, 'tag': line.strip().split(' ')[0][1:], 'index': index + 1, 'element': 'container'})
        finalArray.append({'id': numElem, 'type': 'container', 'name': 'container', 'show': False, 'content': [{'id': numElem + 1, 'type': 'row', 'name': 'Row', 'canDelete': False, 'content': []}]})
        numElem += 2
      elif len(stack) > 2 and canSave and re.search(r'<img', line):
        # add img tags
        continue
      elif len(stack) > 2 and canSave and (re.search(r'id="page\d+_htmltext\d+"', line) or re.search(r'id="page\d+_title\d+"', line)):
        # Add every row in inner tags
        stack.append({'tag': line.strip().split(' ')[0][1:], 'index': index + 1, 'element': 'Text'})
        numElem += 1
      elif len(stack) == 2 and canSave:
        # Add every column
        if re.search(r'id="page\d+_htmltext\d+"', line) or re.search(r'id="page\d+_title\d+"', line):
          stack.append({'tag': line.strip().split(' ')[0][1:], 'index': index + 1, 'element': 'Text'})
        if re.search(r'<a ', line):
          continue
        else:
          addRow(finalArray[-1], getStackId())
          stack.append({'id': numElem, 'tag': line.strip().split(' ')[0][1:], 'index': index + 1, 'element': 'column'})
          numElem += 1
      elif len(stack) > 2 and canSave and stack[-1].get('flag') == 1:
        # First tags of new rows
        addRow(finalArray[-1], getStackId())
        stack.append({'id': numElem, 'tag': line.strip().split(' ')[0][1:], 'index': index + 1, 'element': 'column'})
        numElem += 1
      elif len(stack) > 2 and canSave and re.search(r'id="page\d+_container\d+"', line):
        # Add every row in inner tags
        addRow(finalArray[-1], getStackId())
        stack.append({'id': numElem, 'tag': line.strip().split(' ')[0][1:], 'index': index + 1, 'element': 'row', 'flag': 1})
        numElem += 1
      elif len(stack) > 1 and canSave:
        # All other tags
        stack.append({'id': numElem, 'tag': line.strip().split(' ')[0][1:].split('>')[0], 'index': index + 1})
        numElem += 1

newFile.close()

newFile = open('output.json', 'w')
json.dump(finalArray, newFile)
newFile.close()

"""
# DEBUG line by line 
while(True):
  opt = input('')
  if opt == '':
    break
"""
