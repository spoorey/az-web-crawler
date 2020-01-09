// This script was used to assign the vector paths on the map with their respective name label. It can be run from the browser's console
spans = $('tspan');
paths = $('path');
pathIdsAndNames = {};
spans.each(function (i, cSpan) {
    name = (cSpan.textContent).trim()
    cSpan = $('#' + cSpan.id);
    bestPath = null;
    bestDistance = 0;

    // find closest fitting path for this label
    paths.each(function (i, cPath) {

        bbox = document.getElementById(cPath.id).getBBox();
        cPath = $('#' + cPath.id);

        // span must be within the path
        spanPosition = cSpan.position();
        if (
            spanPosition['top'] >= bbox['y']
            && spanPosition['top'] <= (bbox['y'] + bbox['height'])
            && spanPosition['left'] >= bbox['x']
            && spanPosition['left'] <= (bbox['x'] + bbox['width'])
        ) {
            // calculate distance to the top left and bottom right corners of the path
            dy = spanPosition['top'] - bbox['y'];
            dx = spanPosition['left'] - bbox['x'];
            distanceLT = Math.sqrt((dy * dy) + (dx * dx));

            dy = spanPosition['top'] - (bbox['y'] + bbox['height']);
            dx = spanPosition['left'] - (bbox['x'] + bbox['width']);
            distanceRB = Math.sqrt((dy * dy) + (dx * dx));

            distance = distanceLT + distanceRB;

            isShortestDistance = (distance < bestDistance)
            if (isShortestDistance || null == bestPath) {
                bestDistance = distance;
                bestPath = cPath;
            }
        }
    })
    if (bestPath == null) {
        // no matching path was found, user must fix manually
        console.log('nothing for ' + name)
    } else {
        // add the label to the closest path. Some paths have multiple labels due to multiline names
        if (typeof pathIdsAndNames[bestPath.attr('id')] == 'undefined') {
            pathIdsAndNames[bestPath.attr('id')] = name;
        } else {
            if (pathIdsAndNames[bestPath.attr('id')].indexOf(name) == -1) {
                pathIdsAndNames[bestPath.attr('id')] = pathIdsAndNames[bestPath.attr('id')] + name;
            }
        }

    }
});

// for manual checks using browser devtools
for (id in pathIdsAndNames) {
    $('#' + id).attr('name', pathIdsAndNames[id])
}

// this ouptut can be saved to the names-and-ids.json file
console.log(pathIdsAndNames);
