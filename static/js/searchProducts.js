const searchField = document.querySelector("#searchField")
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
tableOutput.style.display = "none";
const tbody = document.querySelector('.table-body');


searchField.addEventListener("keyup", (e) =>{
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        console.log('searchValue', searchValue);

        tbody.innerHTML = "";
        fetch("/search-products", {
            body: JSON.stringify({searchText: searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                appTable.style.display = "none";
                tableOutput.style.display = "block";

                 if(data.length === 0){
                     tableOutput.style.display="none";
                }else{

                     data.forEach((item) => {
                         console.log(item);
                             tbody.innerHTML += `
                         <tr>
                            <td><img src="/media/${item.image}" height="50" weight="50"></td>
                             <td>${item.name}</td>
                             <td>${item.price}</td>
                             <td>${item.shortSpecifications}</td>
                             <td>${item.discount}%</td>
                             <td>${item.year}</td>
                             <td><img src="/media/icons/${item.isActive}.png" height="25" weight="25"></td>
                             <td>${item.category__name}</td>
                             <td>${item.company__name}</td>
                             <td><img src="/media/icons/${item.digital}.png" height="25" weight="25"></td>
                             <td>
                                 <a class="btn btn-warning" href="/update_product/${item.id}">Change</a>
                             </td>
                             <td>
                                 <a class="btn btn-danger" href="/delete_product/${item.id}">Delete</a>
                             </td>                     
                        </tr>`
                     });
                 }

            });
    }
     else{
         tableOutput.style.display="none";
         appTable.style.display = "block";
     }
})