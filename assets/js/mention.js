// Source: https://github.com/component/textarea-caret-position/blob/master/index.js

/* jshint browser: true */

(function () {

// We'll copy the properties below into the mirror div.
// Note that some browsers, such as Firefox, do not concatenate properties
// into their shorthand (e.g. padding-top, padding-bottom etc. -> padding),
// so we have to list every single property explicitly.
var properties = [
  'direction',  // RTL support
  'boxSizing',
  'width',  // on Chrome and IE, exclude the scrollbar, so the mirror div wraps exactly as the textarea does
  'height',
  'overflowX',
  'overflowY',  // copy the scrollbar for IE

  'borderTopWidth',
  'borderRightWidth',
  'borderBottomWidth',
  'borderLeftWidth',
  'borderStyle',

  'paddingTop',
  'paddingRight',
  'paddingBottom',
  'paddingLeft',

  // https://developer.mozilla.org/en-US/docs/Web/CSS/font
  'fontStyle',
  'fontVariant',
  'fontWeight',
  'fontStretch',
  'fontSize',
  'fontSizeAdjust',
  'lineHeight',
  'fontFamily',

  'textAlign',
  'textTransform',
  'textIndent',
  'textDecoration',  // might not make a difference, but better be safe

  'letterSpacing',
  'wordSpacing',

  'tabSize',
  'MozTabSize'

];

var isBrowser = (typeof window !== 'undefined');
var isFirefox = (isBrowser && window.mozInnerScreenX != null);

function getCaretCoordinates(element, position, options) {
  if (!isBrowser) {
    throw new Error('textarea-caret-position#getCaretCoordinates should only be called in a browser');
  }

  var debug = options && options.debug || false;
  if (debug) {
    var el = document.querySelector('#input-textarea-caret-position-mirror-div');
    if (el) el.parentNode.removeChild(el);
  }

  // The mirror div will replicate the textarea's style
  var div = document.createElement('div');
  div.id = 'input-textarea-caret-position-mirror-div';
  document.body.appendChild(div);

  var style = div.style;
  var computed = window.getComputedStyle ? window.getComputedStyle(element) : element.currentStyle;  // currentStyle for IE < 9
  var isInput = element.nodeName === 'INPUT';

  // Default textarea styles
  style.whiteSpace = 'pre-wrap';
  if (!isInput)
    style.wordWrap = 'break-word';  // only for textarea-s

  // Position off-screen
  style.position = 'absolute';  // required to return coordinates properly
  if (!debug)
    style.visibility = 'hidden';  // not 'display: none' because we want rendering

  // Transfer the element's properties to the div
  properties.forEach(function (prop) {
    if (isInput && prop === 'lineHeight') {
      // Special case for <input>s because text is rendered centered and line height may be != height
      if (computed.boxSizing === "border-box") {
        var height = parseInt(computed.height);
        var outerHeight =
          parseInt(computed.paddingTop) +
          parseInt(computed.paddingBottom) +
          parseInt(computed.borderTopWidth) +
          parseInt(computed.borderBottomWidth);
        var targetHeight = outerHeight + parseInt(computed.lineHeight);
        if (height > targetHeight) {
          style.lineHeight = height - outerHeight + "px";
        } else if (height === targetHeight) {
          style.lineHeight = computed.lineHeight;
        } else {
          style.lineHeight = 0;
        }
      } else {
        style.lineHeight = computed.height;
      }
    } else {
      style[prop] = computed[prop];
    }
  });

  if (isFirefox) {
    // Firefox lies about the overflow property for textareas: https://bugzilla.mozilla.org/show_bug.cgi?id=984275
    if (element.scrollHeight > parseInt(computed.height))
      style.overflowY = 'scroll';
  } else {
    style.overflow = 'hidden';  // for Chrome to not render a scrollbar; IE keeps overflowY = 'scroll'
  }

  div.textContent = element.value.substring(0, position);
  // The second special handling for input type="text" vs textarea:
  // spaces need to be replaced with non-breaking spaces - http://stackoverflow.com/a/13402035/1269037
  if (isInput)
    div.textContent = div.textContent.replace(/\s/g, '\u00a0');

  var span = document.createElement('span');
  // Wrapping must be replicated *exactly*, including when a long word gets
  // onto the next line, with whitespace at the end of the line before (#7).
  // The  *only* reliable way to do that is to copy the *entire* rest of the
  // textarea's content into the <span> created at the caret position.
  // For inputs, just '.' would be enough, but no need to bother.
  span.textContent = element.value.substring(position) || '.';  // || because a completely empty faux span doesn't render at all
  div.appendChild(span);

  var coordinates = {
    top: span.offsetTop + parseInt(computed['borderTopWidth']),
    left: span.offsetLeft + parseInt(computed['borderLeftWidth']),
    height: parseInt(computed['lineHeight'])
  };

  if (debug) {
    span.style.backgroundColor = '#aaa';
  } else {
    document.body.removeChild(div);
  }

  return coordinates;
}

if (typeof module != 'undefined' && typeof module.exports != 'undefined') {
  module.exports = getCaretCoordinates;
} else if(isBrowser) {
  window.getCaretCoordinates = getCaretCoordinates;
}

}());

// Create a dropdown.
var dropdown = document.createElement('div');
dropdown.id = 'mention-dropdown';
dropdown.classList.add('list-group', 'd-none');
dropdown.style.position = 'absolute';
dropdown.style.maxHeight = '200px';
dropdown.style.minWidth = '200px';
dropdown.style.maxWidth = '300px';
dropdown.style.overflowY = 'auto';
document.body.appendChild(dropdown);

$("#id_content").on('keyup', function(event) {
  var textarea = document.getElementById('id_content');

  // Exit if there are no mentions.
  if (!textarea.value.includes('@')) {
    // Hide the dropdown.
    dropdown.classList.remove('d-block');
    dropdown.classList.add('d-none');
    return;
  };

  // Get the cursor position.
  var cursorPosition = textarea.selectionEnd;

  // Replace newlines with spaces.
  var textareaWords = textarea.value.replaceAll("\n", " ");
  // Split the textarea contents into an array and get the words that contain '@'.
  // Get the textarea words into an array.
  textareaWords = textareaWords.split(" ");
  var textareaMentions = [];

  textareaWords.forEach(function(word) {
    if (word.includes('@')) {
      // Get this word's position in the textarea.
      // Add '@' in case it comes at the end of the word.
      let position = textarea.value.indexOf(word) + word.indexOf('@');
      textareaMentions.push({'word': word, 'position': position});
    };
  });

  var nearestMention = {};
  // Check the position of each mention and find which one is nearest to the cursor.
  textareaMentions.forEach(function(mention) {
    let distanceFromCursor = Math.abs(mention.position - cursorPosition);
    // If nearestMention is empty, then this is automatically the nearest mention.
    // Or, if this mention is less distance from the cursor than the previous one,
    // this is the new nearest mention.
    if (
      Object.keys(nearestMention).length === 0 ||
      distanceFromCursor < nearestMention.distance
    ) {
      nearestMention = {
        'word': mention.word,
        'position': mention.position,
        'distance': distanceFromCursor
      };
    };
  });

  mentionItems = [];
  // Populate the dropdown with the first 10 results since we have no search word.
  var search = nearestMention.word.split('@')[1];
  if (search != '') {
    search = search.replace('@', '');
  };
  if (search.length === 0) {
    mentionItems = dropdownItems.slice(0, 10);
  } else {
    // Get similar items from the dictionary and add them to the dropdown.
    dropdownItems.forEach(function(obj) {
      if (obj.name.includes(search)) {
        mentionItems.push(obj);
      };
    });
  };

  // Check if there are any matching dropdown items. Exit if there aren't any matches.
  if (mentionItems.length === 0) {
    // Hide the dropdown.
    dropdown.classList.remove('d-block');
    dropdown.classList.add('d-none');
    return;
  };

  // Empty the dropdown so we can add new items.
  dropdown.innerHTML = '';

  // Show a list of objects that have the lastWord in them.
  var caret = getCaretCoordinates(textarea, nearestMention.position);
  // Bug if textarea is scrolled past initial height.
  var textareaHeight = parseInt(textarea.style.height.replace('px', ''));
  if (textarea.scrollHeight > textareaHeight) {
      let scrollDifference = textarea.scrollHeight - textareaHeight;
      caret.top -= textarea.scrollTop;
  }

  mentionItems.forEach(function(obj) {
    var dropdownItem = document.createElement('a');
    dropdownItem.classList.add('list-group-item', 'list-group-item-action', 'py-1', 'small');
    dropdownItem.href = obj.url;
    dropdownItem.innerHTML = obj.name;
    dropdown.appendChild(dropdownItem);
  });

  // Place it at the textarea's offset plus the caret position.
  dropdown.style.top = textarea.offsetTop + caret.top + 16 + 4 + 'px';
  dropdown.style.left = textarea.offsetLeft + caret.left + 'px';

  // Show the dropdown.
  dropdown.classList.remove('d-none');
  dropdown.classList.add('d-block');

  document.querySelectorAll('.list-group-item').forEach(function(obj) {
    obj.addEventListener('click', function(e) {
      e.preventDefault();

      // Remove the '@' and insert the mention, plus a space at the end.
      const url = `[${this.innerHTML}](${this.href})`;
      // To replace the word, find the @word and replace it with the url.
      textarea.value = textarea.value.replace(`@${search}`, url);
      // Check if the user pressed Spacebar to select the first option.
      if (event.keyCode != 32) {
        textarea.value += ' ';
      };

      // Hide the dropdown.
      dropdown.classList.remove('d-block');
      dropdown.classList.add('d-none');

      // Set the cursor to the end of the textarea.
      cursorPosition += url.length;
      textarea.focus();
      textarea.setSelectionRange(cursorPosition, cursorPosition);
    });
  });

  // Select the first focus item by pressing Spacebar.
  if (event.keyCode == 32) {
    dropdown.firstElementChild.focus();
    dropdown.firstElementChild.click();
  };
});
