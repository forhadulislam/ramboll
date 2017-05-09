<template>
  <div class="hello">
    <ul>
    </ul>
	
	<div class="row">
		<div class="col-md-4">
			<form>
				Stops
				<select class="selectpicker" data-live-search="true">
				  <option data-tokens="ketchup mustard">Hot Dog, Fries and a Soda</option>
				  <option data-tokens="mustard">Burger, Shake and a Smile</option>
				  <option data-tokens="frosting">Sugar, Spice and all things nice</option>
				</select>

			</form>
		 {{ events }}
		</div>
		
		<div class="col-md-8">
		
		
		</div>
	</div>
  </div>
</template>

<script>
export default {
	name: 'hello',
	
	data () {
		return {
		  msg: 'Welcome to Your Vue.js App',
		  allStops: [],
		  events: []
		}
	},
	ready: function() {
		this.getStops();
	},
	methods:{

		getStops: function(){			
				
				this.$http.get('http://127.0.0.1:5000/api/v1/get-stopid', function(allStops){
					this.$set('allStops', allStops)
				});
				
				var events = [
					  {
						id: 1,
						name: 'TIFF',
						description: 'Toronto International Film Festival',
						date: '2015-09-10'
					  },
					  {
						id: 2,
						name: 'The Martian Premiere',
						description: 'The Martian comes to theatres.',
						date: '2015-10-02'
					  },
					  {
						id: 3,
						name: 'SXSW',
						description: 'Music, film and interactive festival in Austin, TX.',
						date: '2016-03-11'
					  }
					];
				this.$set('events', events);
		} 
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
