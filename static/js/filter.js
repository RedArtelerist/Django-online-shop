function ajaxSend(url, params) {
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => render(json))
        .catch(error => console.error(error))
}

const forms = document.querySelector('form[name=filter]');
 forms.addEventListener('submit', function (e) {
     e.preventDefault();
     let url = this.action;
     let params = new URLSearchParams(new FormData(this)).toString();
     console.log(url)
     console.log(params)
     ajaxSend(url, params);
 });

function render(data) {
    // Рендер шаблона
    //console.log(data);
    //console.log(data.products[0].name);
    let template = Hogan.compile(html);
    //var template = require('swig')
    //var tmpl = template.compileFile(html);
    //var template = Swig.compile(html)
    let output = template.render(data);

    const div = document.querySelector('.products-list>.row');
    div.innerHTML = output;

    //document.querySelector('.class1').innerHTML = data.producrs
}

let html = '\
{{#products}}\
    <div class="col-md-4 product-item">\
      <div class="card mb-4 shadow-sm">\
          <div class="image">\
              <a href="/product/{{id}}">\
                  <img class="thumbnail" alt="{{name}}" title="{{name}}" src="media/{{image}}">\
              </a>\
          </div>\
          <div class="card-body">\
              <a href="/product/{{id}}" style="text-decoration: none; color: black">\
                  <p class="card-text"><strong>{{name}}</strong></p>\
              </a>\
              <hr>\
              <button data-product="{{id}}" data-action="add" class="btn btn-outline-secondary add-btn update-cart">Add to cart</button>\
              <a class="btn btn-outline-success" href="/product/{{id}}">View</a>\
              {{#discount}}\
                  <span class="discount">-{{ discount }}%</span>\
                  <div class="price">\
                      <p class="product-price" style="text-decoration: line-through; opacity: .7;">${{ price }}</p>\
                      <p class="product-discount-price">${{ discount_price}}</p>\
                  </div>\
              {{/discount}}\
              {{^discount}}\
                 <div class="price">\
                     <p class="product-price" style="font-weight: 700;">${{price}}</p>\
                  </div>\
              {{/discount}}\
                <div style="display: flex">\
                    <div style="color: orange;" class="product-rating">\
                        <i class="fa fa-star{{ #average_review < 1}}-o empty{{ /if}}"></i>\
                        <i class="fa fa-star{{ #average_review < 2}}-o empty{{ /if}}"></i>\
                        <i class="fa fa-star{{ #average_review < 3}}-o empty{{ /if}}"></i>\
                        <i class="fa fa-star{{ #average_review < 4}}-o empty{{ /if}}"></i>\
                        <i class="fa fa-star{{ #average_review < 5}}-o empty{{ /if}}"></i>\
                        {{average_review}}\
                    </div>\
                    <div style="margin-left: 10px"> {{ count_review }} Review(s)</div>\
                </div>\
          </div>\
          <div class="info">\
              <div class="info_text">\
                  <p>\
                      <strong>Specifications:</strong><br>\
                        {{shortSpecifications}}\
                  </p>\
              </div>\
          </div>\
      </div>\
  </div>\
{{/products}}'

/*let html = '{% for product in products %}\n' +
    '                      <div class="col-md-4 product-item">\n' +
    '                          <div class="card mb-4 shadow-sm">\n' +
    '                              <div class="image">\n' +
    '                                  <a href="{% url \'product\' product.id %}">\n' +
    '                                      <img class="thumbnail" alt="{{product.name}}" title="{{product.name}}" src="{{product.imageURL}}">\n' +
    '                                  </a>\n' +
    '                              </div>\n' +
    '                              <div class="card-body">\n' +
    '                                  <a href="{% url \'product\' product.id %}" style="text-decoration: none; color: black">\n' +
    '                                      <p class="card-text"><strong>{{product.name}}</strong></p>\n' +
    '                                  </a>\n' +
    '                                  <hr>\n' +
    '                                  <button data-product="{{product.id}}" data-action="add" class="btn btn-outline-secondary add-btn update-cart">Add to cart</button>\n' +
    '                                  <a class="btn btn-outline-success" href="{% url \'product\' product.id %}">View</a>\n' +
    '                                  {% if product.discount %}\n' +
    '                                      <span class="discount">-{{ product.discount }}%</span>\n' +
    '                                      <div class="price">\n' +
    '                                          <p class="product-price" style="text-decoration: line-through; opacity: .7;">${{ product.price}}</p>\n' +
    '                                          <p class="product-discount-price">${{ product.discount_price|floatformat:2 }}</p>\n' +
    '                                      </div>\n' +
    '                                  {% else %}\n' +
    '                                     <div class="price">\n' +
    '                                         <p class="product-price" style="font-weight: 700;">${{ product.price|floatformat:2}}</p>\n' +
    '                                      </div>\n' +
    '                                  {% endif %}\n' +
    '                                    <div style="display: flex">\n' +
    '                                        <div style="color: orange;" class="product-rating">\n' +
    '                                            <i class="fa fa-star{% if product.average_review < 1 %}-o empty{% endif%}"></i>\n' +
    '                                            <i class="fa fa-star{% if product.average_review < 2 %}-o empty{% endif%}"></i>\n' +
    '                                            <i class="fa fa-star{% if product.average_review < 3 %}-o empty{% endif%}"></i>\n' +
    '                                            <i class="fa fa-star{% if product.average_review < 4 %}-o empty{% endif%}"></i>\n' +
    '                                            <i class="fa fa-star{% if product.average_review < 5 %}-o empty{% endif%}"></i>\n' +
    '                                            {{ product.average_review |stringformat:".2f"}}\n' +
    '                                        </div>\n' +
    '                                        <div style="margin-left: 10px"> {{ product.count_review}} Review(s)</div>\n' +
    '                                    </div>\n' +
    '                              </div>\n' +
    '\n' +
    '                              <div class="info">\n' +
    '                                  <div class="info_text">\n' +
    '                                      <p>\n' +
    '                                          <strong>Specifications:</strong><br>\n' +
    '                                            {{product.shortSpecifications|safe}}\n' +
    '                                      </p>\n' +
    '                                  </div>\n' +
    '                              </div>\n' +
    '\n' +
    '                          </div>\n' +
    '                      </div>\n' +
    '                  {% endfor %}' */