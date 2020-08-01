const SCORE_EXPONENTIAL = 8;

const BASE_URL = 'http://localhost:8080';

fetch(`${BASE_URL}/api/player/maliiik`)
    .then((response) => response.json())
    .then((response) => {
        document.title = response
    });

fetch(`${BASE_URL}/api/team`)
    .then((response) => response.json())
    .then((response) => {
        const teamNames = Object.keys(response);
        teamNames.forEach((teamName) => response[teamName].winEfficiency = response[teamName].wins / response[teamName].rating19_20);
        teamNames.sort((a, b) => response[b].winEfficiency - response[a].winEfficiency);
        scaleValues(response, 'winEfficiency');
        scaleValues(response, 'rating19_20');
        scaleValues(response, 'totalRating');
        const table = document.getElementById('teamTable');
        const tableBody = table.getElementsByTagName('tbody')[0];
        for (teamName of teamNames) {
            const newRow = tableBody.insertRow(tableBody.rows.length);
            const teamCell = newRow.insertCell(0);
            const winEfficiencyCell = newRow.insertCell(1);
            const rating19_20 = newRow.insertCell(2);
            const winsCell = newRow.insertCell(3);
            const totalRatingCell = newRow.insertCell(4);
            teamCell.appendChild(document.createTextNode(teamName));
            winEfficiencyCell.appendChild(document.createTextNode(response[teamName].winEfficiency));
            rating19_20.appendChild(document.createTextNode(response[teamName].rating19_20));
            winsCell.appendChild(document.createTextNode(response[teamName].wins));
            totalRatingCell.appendChild(document.createTextNode(response[teamName].totalRating));
        }
        table.style.display = 'table';
        document.getElementById('loading').style.display = 'none';
    });

fetch(`${BASE_URL}/api/player`)
    .then((response) => response.json())
    .then((response) => {
        const playerNames = Object.keys(response);
        playerNames.forEach((playerName) => response[playerName].value19_20 = (response[playerName].rating ** SCORE_EXPONENTIAL) * response[playerName].minutesPlayed);
        playerNames.sort((a, b) => response[b].rating - response[a].rating);
        scaleValues(response, 'value19_20');
        const table = document.getElementById('playerTable');
        const tableBody = table.getElementsByTagName('tbody')[0];
        for (playerName of playerNames) {
            const newRow = tableBody.insertRow(tableBody.rows.length);
            const nameCell = newRow.insertCell(0);
            const ratingCell = newRow.insertCell(1);
            const teamCell = newRow.insertCell(2);
            const value19_20Cell = newRow.insertCell(3);
            const minutesCell = newRow.insertCell(4);
            nameCell.appendChild(document.createTextNode(formatName(playerName)));
            ratingCell.appendChild(document.createTextNode(response[playerName].rating));
            teamCell.appendChild(document.createTextNode(response[playerName].teamName));
            value19_20Cell.appendChild(document.createTextNode((response[playerName].value19_20)));
            minutesCell.appendChild(document.createTextNode(response[playerName].minutesPlayed));
        }
        table.style.display = 'table';
        document.getElementById('loading').style.display = 'none';
    });

function scaleValues(object, propertyName) {
    let
        max = Number.MAX_VALUE * -1,
        min = Number.MAX_VALUE;
    Object.keys(object).forEach((key) => {
        property = object[key][propertyName];
        if (property < min) {
            min = property;
        }
        if (property > max) {
            max = property;
        }
    });
    Object.keys(object).forEach((key) => {
        object[key][propertyName] = Math.round(10000 * (object[key][propertyName] - min) / (max - min)) / 100;
    });
}

function formatName(name) {
    return name
        .split(' ')
        .map((split) => split.charAt(0).toUpperCase() + split.slice(1))
        .join(' ');
}