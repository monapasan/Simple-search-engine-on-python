/** @jsx React.DOM */

    var DynamicSearch = React.createClass({

      // sets initial state
      getInitialState: function(){
        return { searchString: '' };
      },

      // sets state, triggers render method
      handleChange: function(event){
        // grab value form input box
        this.setState({searchString:event.target.value});
      },
      handleSearch:function(){
          var searchString = this.state.searchString.trim().toLowerCase();
          console.log(searchString);
          this.handleTaskSubmit(searchString);
      },
      handleTaskSubmit: function (searchString) {
          $.ajax({
              type: "POST",
              url: '/',
              data: {'query': searchString},
              success: this.successQuery,
              error: function (xhr, status, err) {
                  console.error( status, err.toString());
              }.bind(this)
          });
      },
      successQuery:function(data){
          this.setState({searchResults: data});
      },
      render: function() {

        var countries = this.props.items;
        var searchString = this.state.searchString.trim().toLowerCase();
        var WithRanking = [];
        var CosineScore = [];
        var PageRank = [];
        if(this.state.searchResults){
            WithRanking = this.state.searchResults.WithRanking;
            CosineScore = this.state.searchResults.CosineScore;
            PageRank = this.state.searchResults.PageRank;
        }
        //   { countries.map(function(country){ return <li>{country.name} </li>; }) }

        // filter countries list by value from input box
        if(searchString.length > 0){
          countries = countries.filter(function(country){
            return country.name.toLowerCase().match( searchString );
          });
        }
        return (
          <div>
            <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
            <button  onClick={this.handleSearch}> Search </button>
            <ul>
              {WithRanking.map(function(res, i){
                  return <li>{res[0]}
                    <p>WithRanking : {res[1]}</p>
                    <p>PageRank : {PageRank[res[0]]}</p>
                    <p>CosineScore : {CosineScore[i][1]}</p>
                    </li>;
              })}
            </ul>
          </div>
      );
      }

    });

    // list of countries, defined with JavaScript object literals
    var countries = [
      {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
      {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
      {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
      {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
      {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
      {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
      {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
    ];

    React.render(
      <DynamicSearch items={ countries } />,
      document.getElementById('main')
    );
