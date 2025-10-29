
RULE PROMPT
```text
1. Each line consists of only one piece of fact, possibly there could be explanation of the formula after a hashtag #.\n
2. Predicates are named in terms of properties such as location, color, size etc. Connect words with underline. Use lowercases only.\n
3. Objects and quantities are given as arguments of the predicates (use irrel if the object is uncountable or the number is irrelevant). Connect words with underline and always use singular form\n
4. Logical connectives such as AND, OR, or NOT might be used.
5. Description is given in form 'TEXT: (Description of the image)' and output should be in form 'FORMULA: (a set of logical formulae)'.
6. Use only the following predicates:
color($object$, $color$) # $object$ has a certain $color$
fruit_label($fruit$) # if a label with an icon of $fruit$ is mentioned
volume($description$) # the volume satisfies the $description$
sticker_at($description$, $location$) # a sticker satisfying the $description$ is at the $location$
image_on_label($location$) # the $location$ of the image on the label
juice_fruit_match(irrel) # the color of the juice and the label of fruit match with each other
count($object$, $number$) # the $number$ of the $object$
is_symmetrical(irrel) # The bottle with stickers is symmetrical
```

```json
{
  "type": "object",
  "required": ["color","fruit_label","volume","stickers"],
  "properties": {
    "color": {
      "type": "object",
      "required": ["target","value"],
      "properties": {
        "target": {"type":"string","enum":["juice"]},
        "value": {"type":"string"}
      }
    },
    "fruit_label": {"type":"string"},
    "volume": {"type":"string","enum":["around_half_neck","full","empty","unknown"]},
    "stickers": {
      "type": "object",
      "required": ["count","top","bottom"],
      "properties": {
        "count": {"type":"integer","minimum":0},
        "top": {
          "type":"object",
          "required":["present"],
          "properties":{
            "present":{"type":"boolean"},
            "type":{"type":["string","null"]},
            "valid":{"type":["boolean","null"]}
          }
        },
        "bottom": {
          "type":"object",
          "required":["present"],
          "properties":{
            "present":{"type":"boolean"},
            "type":{"type":["string","null"]},
            "valid":{"type":["boolean","null"]}
          }
        },
        "symmetrical":{"type":["boolean","null"]}
      }
    },
    "constraints": {
      "type":"object",
      "properties":{
        "juice_fruit_match":{"type":"string","enum":["yes","no","unknown"]},
        "image_on_label":{"type":"string","enum":["top","middle","bottom","unknown"]}
      }
    }
  }
}

```