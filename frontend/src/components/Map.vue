<template>
    <div class="title">
        <h1>Server Locations</h1>
        <p>
        lorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsum
        lorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsumlorem ipsum
        </p>
    </div>

    <div class="world-map">
        <img src="../assets/worldmap.png" alt="map"/>
        <div class="pin usa">
            <span>United States</span>
        </div>
        <div class="pin france">
            <span>France</span>
        </div>
        <div class="pin sweden">
            <span>Sweden</span>
        </div>
        <div class="pin south-africa">
            <span>South Africa</span>
        </div>
        <div class="pin brazil">
            <span>Brazil</span>
        </div>
        <div class="pin china">
            <span>China</span>
        </div>
        <div class="pin australia">
            <span>Australia</span>
        </div>
    </div>
</template>

<style scoped>
body {
    margin: 0;
    font-family: sans-serif;
    background: #101224;
}

* {
    box-sizing: border-box;
}
.world-map {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding: 1em;
    position: relative;
}

.world-map img {
    width: 100%;
    height: 100%;
    object-fit: contain
}

.title {
    text-align: center;
    color: #fff;
    margin: 2em 0;
    padding: 0 1em;
}

.title p {
    max-width: 500px;
    margin: 1em auto;
    line-height: 27px;
}

.pin {
    background: #4362f8;
    position: absolute;
    width: 0.7em;
    height: 0.7em;
    border-radius: 50%;
}
</style>