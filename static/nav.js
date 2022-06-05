
/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
    document.getElementById("main").style.marginLeft = "300px";
  }
  
  /* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }

  function build_industry_dropdown(){
    industries = ['Advertising Agencies',
  'Aerospace & Defense',
  'Agricultural Inputs',
  'Airlines',
  'Airports & Air Services',
  'Aluminum',
  'Apparel Manufacturing',
  'Apparel Retail',
  'Asset Management',
  'Auto & Truck Dealerships',
  'Auto Manufacturers',
  'Auto Parts',
  'Banks - Diversified',
  'Banks - Regional',
  'Beverages - Brewers',
  'Beverages - Non-Alcoholic',
  'Beverages - Wineries & Distilleries',
  'Biotechnology',
  'Broadcasting',
  'Building Materials',
  'Building Products & Equipment',
  'Business Equipment & Supplies',
  'Capital Markets',
  'Chemicals',
  'Coking Coal',
  'Communication Equipment',
  'Computer Hardware',
  'Confectioners',
  'Conglomerates',
  'Consulting Services',
  'Consumer Electronics',
  'Copper',
  'Credit Services',
  'Department Stores',
  'Diagnostics & Research',
  'Discount Stores',
  'Drug Manufacturers - General',
  'Drug Manufacturers - Specialty & Generic',
  'Education & Training Services',
  'Electrical Equipment & Parts',
  'Electronic Components',
  'Electronic Gaming & Multimedia',
  'Electronics & Computer Distribution',
  'Engineering & Construction',
  'Entertainment',
  'Farm & Heavy Construction Machinery',
  'Farm Products',
  'Financial Conglomerates',
  'Financial Data & Stock Exchanges',
  'Food Distribution',
  'Footwear & Accessories',
  'Furnishings, Fixtures & Appliances',
  'Gambling',
  'Gold',
  'Grocery Stores',
  'Health Information Services',
  'Healthcare Plans',
  'Home Improvement Retail',
  'Household & Personal Products',
  'Industrial Distribution',
  'Information Technology Services',
  'Insurance - Diversified',
  'Insurance - Life',
  'Insurance - Property & Casualty',
  'Insurance - Reinsurance',
  'Insurance - Specialty',
  'Insurance Brokers',
  'Integrated Freight & Logistics',
  'Internet Content & Information',
  'Internet Retail',
  'Leisure',
  'Lodging',
  'Lumber & Wood Production',
  'Luxury Goods',
  'Marine Shipping',
  'Medical Care Facilities',
  'Medical Devices',
  'Medical Distribution',
  'Medical Instruments & Supplies',
  'Metal Fabrication',
  'Mortgage Finance',
  'Oil & Gas Drilling',
  'Oil & Gas E&P',
  'Oil & Gas Equipment & Services',
  'Oil & Gas Integrated',
  'Oil & Gas Midstream',
  'Oil & Gas Refining & Marketing',
  'Other Industrial Metals & Mining',
  'Other Precious Metals & Mining',
  'Packaged Foods',
  'Packaging & Containers',
  'Paper & Paper Products',
  'Personal Services',
  'Pharmaceutical Retailers',
  'Pollution & Treatment Controls',
  'Publishing',
  'REIT - Diversified',
  'REIT - Healthcare Facilities',
  'REIT - Hotel & Motel',
  'REIT - Industrial',
  'REIT - Mortgage',
  'REIT - Office',
  'REIT - Residential',
  'REIT - Retail',
  'REIT - Specialty',
  'Railroads',
  'Real Estate - Development',
  'Real Estate - Diversified',
  'Real Estate Services',
  'Recreational Vehicles',
  'Rental & Leasing Services',
  'Residential Construction',
  'Resorts & Casinos',
  'Restaurants',
  'Scientific & Technical Instruments',
  'Security & Protection Services',
  'Semiconductor Equipment & Materials',
  'Semiconductors',
  'Shell Companies',
  'Silver',
  'Software - Application',
  'Software - Infrastructure',
  'Solar',
  'Specialty Business Services',
  'Specialty Chemicals',
  'Specialty Industrial Machinery',
  'Specialty Retail',
  'Staffing & Employment Services',
  'Steel',
  'Telecom Services',
  'Textile Manufacturing',
  'Thermal Coal',
  'Tobacco',
  'Tools & Accessories',
  'Travel Services',
  'Trucking',
  'Uranium',
  'Utilities - Diversified',
  'Utilities - Independent Power Producers',
  'Utilities - Regulated Electric',
  'Utilities - Regulated Gas',
  'Utilities - Regulated Water',
  'Utilities - Renewable',
  'Waste Management'];

//if url contains variable industry, then show back button  
console.log(window.location.href)
//if (window.location.href.indexOf("?industry=") == -1){
if (window.location.href.indexOf("?industry=") == -1){
  var _btn = document.getElementById("btn_goback");
  if (_btn){
    _btn.innerText = "abc";
    _btn.style.display = "none";
  }
}

  var industry_dropdown = document.getElementById('industry_dropdown');

  for (const val of industries)
    {
        var option = document.createElement("option");
        option.value = val;
        option.text = val.charAt(0).toUpperCase() + val.slice(1);
        industry_dropdown.add(option);
    }
  } 


