spans = $('tspan');
paths = $('path');
pathIdsAndNames = {};
spans.each(function (i, cSpan) {
    name = (cSpan.textContent).trim()
    cSpan = $('#' + cSpan.id);
    bestPath = null;
    bestDistance = 0;

    // find closest path
    paths.each(function (i, cPath) {

        bbox = document.getElementById(cPath.id).getBBox();
        cPath = $('#' + cPath.id);

        spanPosition = cSpan.position();
        if (
            spanPosition['top'] >= bbox['y']
            && spanPosition['top'] <= (bbox['y'] + bbox['height'])
            && spanPosition['left'] >= bbox['x']
            && spanPosition['left'] <= (bbox['x'] + bbox['width'])
        ) {
            dy = spanPosition['top'] - bbox['y'];
            dx = spanPosition['left'] - bbox['x'];
            distance = distanceLT = Math.sqrt((dy * dy) + (dx * dx));

            ///*
            dy = spanPosition['top'] - (bbox['y'] + bbox['height']);
            dx = spanPosition['left'] - (bbox['x'] + bbox['width']);
            distanceRB = Math.sqrt((dy * dy) + (dx * dx));

            distance = distanceLT + distanceRB;
            //*/

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
        if (typeof pathIdsAndNames[bestPath.attr('id')] == 'undefined') {
            pathIdsAndNames[bestPath.attr('id')] = name;
        } else {
            if (pathIdsAndNames[bestPath.attr('id')].indexOf(name) == -1) {
                pathIdsAndNames[bestPath.attr('id')] = pathIdsAndNames[bestPath.attr('id')] + name;
            }
        }

    }
});

// for manual checks using browser console
for (id in pathIdsAndNames) {
    $('#' + id).attr('name', pathIdsAndNames[id])
}

// this ouptut can be saved to the json file
console.log(pathIdsAndNames);
