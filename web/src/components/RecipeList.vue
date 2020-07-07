<template>
  <ul class="cards">
    <li
      v-for="recipe in recipes"
      :key="recipe.id">
      <a :href="recipe.url">
        <img :src="recipe.image" :alt="recipe.name">
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'RecipeList', 
  data () {
    return {
      recipes: [
        {
          id: 1,
          name: "Creamy Avocado Macaroni Salad",
          url: "https://www.thefullhelping.com/creamy-avocado-macaroni-salad/",
          image: "https://www.thefullhelping.com/wp-content/uploads/2020/07/Creamy-Avocado-Macaroni-Salad-3.jpg"
        },
        {
          id: 2,
          name: 'Vegan Chocolate Cherry Ice Cream',
          url: 'https://www.thefullhelping.com/vegan-chocolate-cherry-ice-cream/',
          image: "https://www.thefullhelping.com/wp-content/uploads/2020/06/Dark-chocolate-cherry-ice-cream-1.jpg"
        },
        {
          id: 3,
          name: "Smoky Glazed Carrot Dogs",
          url: "https://www.thefullhelping.com/smoky-glazed-carrot-dogs/",
          image: "https://www.thefullhelping.com/wp-content/uploads/2020/06/Sweet-smoky-glazed-carrot-dogs-4.jpg"
        },
        {
          id: 4,
          name: 'Sheet Pan Tamari Glazed Tempeh & Broccoli',
          url: 'https://www.thefullhelping.com/sheet-pan-glazed-tempeh-broccoli/',
          image: "https://www.thefullhelping.com/wp-content/uploads/2019/05/Sheet-pan-tempeh-broccoli-5.jpg"
        },
        {
          id: 5,
          name: 'Roasted Broccoli & Kimchi Spicy Soba Noodle Toss',
          url: 'https://www.thefullhelping.com/roasted-broccoli-kimchi-spicy-soba-noodle-toss/',
          image: 'https://www.thefullhelping.com/wp-content/uploads/2018/04/Roasted-broccoli-kimchi-soba-noodle-toss-5.jpg'
        },
        {
          id: 6,
          name: 'Cinnamon Spice Sheet Cake with Cream Cheese Frosting',
          url: 'https://www.thefullhelping.com/cinnamon-spice-sheet-cake-with-cream-cheese-frosting/',
          image: 'https://www.thefullhelping.com/wp-content/uploads/2019/12/Cinnamon-spice-cake-10.jpg'
        },
        {
          id: 7,
          name: 'Easy, Cheesy Vegan Loaded Potatoes with Broccoli & White Beans',
          url: 'https://www.thefullhelping.com/easy-cheesy-vegan-loaded-potatoes-with-broccoli-white-beans/',
          image: 'https://www.thefullhelping.com/wp-content/uploads/2018/12/Cheesy-Stuffed-Potato-6.jpg'
        },
        {
          id: 8,
          name: 'Vegan Beef and Zucchini Stuffed Sweet Potatoes',
          url: 'https://www.thefullhelping.com/vegan-beef-zucchini-stuffed-sweet-potatoes/',
          image: 'https://www.thefullhelping.com/wp-content/uploads/2019/10/Vegan-beef-and-zucchini-stuffed-sweet-potato-2.jpg'
        },
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  list-style-type: none;
}
.cards {
  margin: auto;
  width: 50%;
  text-align: center;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  flex-direction: row;
  max-height: 100vh;
}
.cards > li > a > img {
  margin: 10px;
  border: 3px solid #000;
  box-shadow: 3px 3px 8px 0px rgba(0,0,0,0.3); 
  max-width: 14vw;
}
</style>
