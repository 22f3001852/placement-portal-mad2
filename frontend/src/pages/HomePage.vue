<script>
export default {
    methods:{
        goToLogin: function() {
            this.$router.push('/login')
        }
    }
}
</script>


<template>
<div class="home-canvas">
    <div class="home-card ">
        <h2 class="home-heading">Place<span class="green">Mint</span></h2>
        <h1>Where Ambition Meets Opportunity</h1>
        <h4>Step into a smarter future where opportunities meet ambition. PlaceMint bridges the gap between talented students and forward-thinking companies, creating careers, not just jobs. Empower your journey with a platform designed for growth, connection, and success.</h4>
        <button @click="goToLogin" class="btn btn-primary">Explore</button>
    </div>
</div>
</template>
<style scoped>
.home-canvas {
    height: 90vh;
    width: 100dvw;
    background: #000000;
    background-image: url("@/assets/images/homepageBg.png");
    background-size: cover;
    background-position: center;
    display: flex;
    justify-content: center;
    align-items: center;
    
}
.home-card {
    width: 60%;
    height: 90%;
    background-color: rgba(0, 0, 0, 0.546);
    /* border: 2px solid red; */
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    text-align: center;
    align-items: center;
}

.home-heading {
    color: white;
    font-size: 40px;
    text-align: center;
    margin-top: 20px;
}

.home-card h1 {
    color: white;
    font-family: 'Courier New', Courier, monospace;
    font-size: 52px;
    text-align: center;
    margin-top: 35px;
}
.green {
    color: #008000;
}
.home-card h4 {
    color: rgb(169, 165, 165);
    font-family: 'Verdana', sans-serif;
    font-size: 14px;
    text-align: center;
    margin-top: 20px;
    width: 70%;

}

.btn-primary {
    background-color: #eff5ef2a;
    color: white;
    width: 180px;
    height: 60px;
    border: none;
    border-radius: 20px;
    margin-top: 40px;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    padding-top: 15px;
}
.btn-primary:hover {
    background-color: #05680588;
    color: white;
    /* border: 1px solid #056805; */
    transform: scale(1.05);
}
</style>