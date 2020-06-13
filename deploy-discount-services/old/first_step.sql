-- *************** SqlDBM: PostgreSQL ****************;
-- ***************************************************;

-- ************************************** "shopping_cars"
CREATE TABLE "shopping_cars"
(
 "shopping_car_id" int NOT NULL,
 "name"            varchar(50) NOT NULL,
 CONSTRAINT "PK_shopping_cars" PRIMARY KEY ( "shopping_car_id" )
);

-- ************************************** "prime_suscriptions"
CREATE TABLE "prime_suscriptions"
(
 "prime_suscription_id" int NOT NULL,
 "name"                 varchar(50) NOT NULL,
 "validity"             int NOT NULL,
 "validity_type"        varchar(50) NOT NULL,
 "enabled"              boolean NOT NULL,
 CONSTRAINT "PK_prime_suscriptions" PRIMARY KEY ( "prime_suscription_id" )
);

-- ************************************** "country"
CREATE TABLE "country"
(
 "country_id" int NOT NULL,
 "name"       varchar(50) NOT NULL,
 "code"       varchar(50) NOT NULL,
 "lenguaje"   varchar(50) NOT NULL,
 "currency"   varchar(50) NOT NULL,
 CONSTRAINT "PK_country" PRIMARY KEY ( "country_id" )
);

-- ************************************** "Clients"
CREATE TABLE "Clients"
(
 "client_id" int NOT NULL,
 "name"      varchar(50) NOT NULL,
 "las_name"  varchar(50) NOT NULL,
 "email"     varchar(50) NOT NULL,
 CONSTRAINT "PK_Clients" PRIMARY KEY ( "client_id" )
);

-- ************************************** "categories"
CREATE TABLE "categories"
(
 "category_id" int NOT NULL,
 "name"        varchar(50) NOT NULL,
 "description" text NOT NULL,
 CONSTRAINT "PK_categories" PRIMARY KEY ( "category_id" )
);

-- ************************************** "brands"
CREATE TABLE "brands"
(
 "brand_id" int NOT NULL,
 "name"     varchar(50) NOT NULL,
 CONSTRAINT "PK_brands" PRIMARY KEY ( "brand_id" )
);

-- ************************************** "subcategories"
CREATE TABLE "subcategories"
(
 "subcategory_id" int NOT NULL,
 "name"           varchar(50) NOT NULL,
 "description"    text NOT NULL,
 "category_id"    int NOT NULL,
 CONSTRAINT "PK_subcategories" PRIMARY KEY ( "subcategory_id" ),
 CONSTRAINT "FK_100" FOREIGN KEY ( "category_id" ) REFERENCES "categories" ( "category_id" )
);

CREATE INDEX "fkIdx_100" ON "subcategories"
(
 "category_id"
);

-- ************************************** "province"
CREATE TABLE "province"
(
 "province_id" int NOT NULL,
 "country_id"  int NOT NULL,
 "name"        varchar(50) NOT NULL,
 "region"      varchar(50) NOT NULL,
 CONSTRAINT "PK_province" PRIMARY KEY ( "province_id" ),
 CONSTRAINT "FK_41" FOREIGN KEY ( "country_id" ) REFERENCES "country" ( "country_id" )
);

CREATE INDEX "fkIdx_41" ON "province"
(
 "country_id"
);

-- ************************************** "products"
CREATE TABLE "products"
(
 "product_id"  int NOT NULL,
 "name"        varchar(50) NOT NULL,
 "description" text NOT NULL,
 "tax_rate"    decimal NOT NULL,
 "brand_id"    int NOT NULL,
 CONSTRAINT "PK_products" PRIMARY KEY ( "product_id" ),
 CONSTRAINT "FK_159" FOREIGN KEY ( "brand_id" ) REFERENCES "brands" ( "brand_id" )
);

CREATE INDEX "fkIdx_159" ON "products"
(
 "brand_id"
);

-- ************************************** "clients_prime_suscriptions"
CREATE TABLE "clients_prime_suscriptions"
(
 "id" int NOT NULL,
 "prime_suscription_id" int NOT NULL,
 "client_id"            int NOT NULL,
 "activation_date"      date NOT NULL,
 "suscription_state"    varchar(50) NOT NULL,
 CONSTRAINT "PK_clients_prime_suscriptions" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_23" FOREIGN KEY ( "client_id" ) REFERENCES "Clients" ( "client_id" ),
 CONSTRAINT "FK_26" FOREIGN KEY ( "prime_suscription_id" ) REFERENCES "prime_suscriptions" ( "prime_suscription_id" )
);

CREATE INDEX "fkIdx_23" ON "clients_prime_suscriptions"
(
 "client_id"
);

CREATE INDEX "fkIdx_26" ON "clients_prime_suscriptions"
(
 "prime_suscription_id"
);

-- ************************************** "client_shopping_cars"
CREATE TABLE "client_shopping_cars"
(
 "id" int NOT NULL,
 "shopping_car_id" int NOT NULL,
 "client_id"       int NOT NULL,
 "date_joined"     date NOT NULL,
 "members"         int NOT NULL,
 CONSTRAINT "PK_client_shopping_cars" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_183" FOREIGN KEY ( "shopping_car_id" ) REFERENCES "shopping_cars" ( "shopping_car_id" ),
 CONSTRAINT "FK_189" FOREIGN KEY ( "client_id" ) REFERENCES "Clients" ( "client_id" )
);

CREATE INDEX "fkIdx_183" ON "client_shopping_cars"
(
 "shopping_car_id"
);

CREATE INDEX "fkIdx_189" ON "client_shopping_cars"
(
 "client_id"
);

-- ************************************** "city"
CREATE TABLE "city"
(
 "city_id"   int   NOT NULL,
 "province_id" int NOT NULL,
 "name"        varchar(50) NOT NULL,
 CONSTRAINT "PK_city" PRIMARY KEY ( "city_id" ),
 CONSTRAINT "FK_49" FOREIGN KEY ( "province_id" ) REFERENCES "province" ( "province_id" )
);

CREATE INDEX "fkIdx_49" ON "city"
(
 "province_id"
);

-- ************************************** "sector"
CREATE TABLE "sector"
(
 "sector_id" int NOT NULL,
 "city_id" int  NOT NULL,
 "name"      varchar(50) NOT NULL,
 CONSTRAINT "PK_sector" PRIMARY KEY ( "sector_id" ),
 CONSTRAINT "FK_56" FOREIGN KEY ( "city_id" ) REFERENCES "city" ( "city_id" )
);

CREATE INDEX "fkIdx_56" ON "sector"
(
 "city_id"
);

-- ************************************** "retailers"
CREATE TABLE "retailers"
(
 "retailer_id" int NOT NULL,
 "name"        varchar(50) NOT NULL,
 "description" text NOT NULL,
 "city_id"   int   NOT NULL,
 CONSTRAINT "PK_retailers" PRIMARY KEY ( "retailer_id" ),
 CONSTRAINT "FK_65" FOREIGN KEY ( "city_id" ) REFERENCES "city" ( "city_id" )
);

CREATE INDEX "fkIdx_65" ON "retailers"
(
 "city_id"
);

-- ************************************** "stock_item"
CREATE TABLE "stock_item"
(
 "id" int NOT NULL,
 "retailer_id" int NOT NULL,
 "product_id"  int NOT NULL,
 "pvp"         decimal NOT NULL,
 "margin"      decimal NOT NULL,
 "category_id" int NOT NULL,
 CONSTRAINT "PK_stock_item" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_104" FOREIGN KEY ( "category_id" ) REFERENCES "categories" ( "category_id" ),
 CONSTRAINT "FK_85" FOREIGN KEY ( "retailer_id" ) REFERENCES "retailers" ( "retailer_id" ),
 CONSTRAINT "FK_88" FOREIGN KEY ( "product_id" ) REFERENCES "products" ( "product_id" )
);

CREATE INDEX "fkIdx_104" ON "stock_item"
(
 "category_id"
);

CREATE INDEX "fkIdx_85" ON "stock_item"
(
 "retailer_id"
);

CREATE INDEX "fkIdx_88" ON "stock_item"
(
 "product_id"
);

-- ************************************** "retailer_coverage_sectors"
CREATE TABLE "retailer_coverage_sectors"
(
 "id" int NOT NULL,
 "retailer_id" int NOT NULL,
 "enabled"     boolean NOT NULL,
 "sector_id"   int NOT NULL,
 CONSTRAINT "PK_retailer_coverage_sectors" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_69" FOREIGN KEY ( "retailer_id" ) REFERENCES "retailers" ( "retailer_id" ),
 CONSTRAINT "FK_72" FOREIGN KEY ( "sector_id" ) REFERENCES "sector" ( "sector_id" )
);

CREATE INDEX "fkIdx_69" ON "retailer_coverage_sectors"
(
 "retailer_id"
);

CREATE INDEX "fkIdx_72" ON "retailer_coverage_sectors"
(
 "sector_id"
);

-- ************************************** "retailer_categories"
CREATE TABLE "retailer_categories"
(
 "retailer_id" int NOT NULL,
 "enabled"     boolean NOT NULL,
 "category_id" int NOT NULL,
 CONSTRAINT "PK_retailer_categories" PRIMARY KEY ( "retailer_id" ),
 CONSTRAINT "FK_109" FOREIGN KEY ( "retailer_id" ) REFERENCES "retailers" ( "retailer_id" ),
 CONSTRAINT "FK_113" FOREIGN KEY ( "category_id" ) REFERENCES "categories" ( "category_id" )
);

CREATE INDEX "fkIdx_109" ON "retailer_categories"
(
 "retailer_id"
);

CREATE INDEX "fkIdx_113" ON "retailer_categories"
(
 "category_id"
);

-- ************************************** "Address"
CREATE TABLE "Address"
(
 "adress_id" int NOT NULL,
 "name"      varchar(50) NOT NULL,
 "line_one"  varchar(50) NOT NULL,
 "line_two"  varchar(50) NOT NULL,
 "sector_id" int NOT NULL,
 CONSTRAINT "PK_Address" PRIMARY KEY ( "adress_id" ),
 CONSTRAINT "FK_133" FOREIGN KEY ( "sector_id" ) REFERENCES "sector" ( "sector_id" )
);

CREATE INDEX "fkIdx_133" ON "Address"
(
 "sector_id"
);

-- ************************************** "shopping_cart_items"
CREATE TABLE "shopping_cart_items"
(
 "id"       int NOT NULL,
 "quantity"         int NOT NULL,
 "note_for_shopper" text NOT NULL,
 "shopping_car_id"  int NOT NULL,
 "item_id"      int NOT NULL,
 CONSTRAINT "PK_shopping_cart_items" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_170" FOREIGN KEY ( "shopping_car_id" ) REFERENCES "shopping_cars" ( "shopping_car_id" ),
 CONSTRAINT "FK_173" FOREIGN KEY ( "item_id" ) REFERENCES "stock_item" ( "id" )
);

CREATE INDEX "fkIdx_170" ON "shopping_cart_items"
(
 "shopping_car_id"
);

CREATE INDEX "fkIdx_173" ON "shopping_cart_items"
(
 "item_id"
);

-- ************************************** "client_orders"
CREATE TABLE "client_orders"
(
 "order_id"      int NOT NULL,
 "client_id"     int NOT NULL,
 "retailer_id"   int NOT NULL,
 "total_cost"    decimal NOT NULL,
 "adress_id"     int NOT NULL,
 "delivery_date" date NOT NULL,
 "shipping_cost" decimal NOT NULL,
 CONSTRAINT "PK_client_orders" PRIMARY KEY ( "order_id" ),
 CONSTRAINT "FK_120" FOREIGN KEY ( "client_id" ) REFERENCES "Clients" ( "client_id" ),
 CONSTRAINT "FK_123" FOREIGN KEY ( "retailer_id" ) REFERENCES "retailers" ( "retailer_id" ),
 CONSTRAINT "FK_136" FOREIGN KEY ( "adress_id" ) REFERENCES "Address" ( "adress_id" )
);

CREATE INDEX "fkIdx_120" ON "client_orders"
(
 "client_id"
);

CREATE INDEX "fkIdx_123" ON "client_orders"
(
 "retailer_id"
);

CREATE INDEX "fkIdx_136" ON "client_orders"
(
 "adress_id"
);

-- ************************************** "order_items"
CREATE TABLE "order_items"
(
 "id"          int NOT NULL,
 "order_id"          int NOT NULL,
 "item_id"       int NOT NULL,
 "pvp"               decimal NOT NULL,
 "quantity"          int NOT NULL,
 "note_for_shopper"  text NOT NULL,
 "pvp_with_disocunt" decimal NOT NULL,
 CONSTRAINT "PK_order_items" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_140" FOREIGN KEY ( "order_id" ) REFERENCES "client_orders" ( "order_id" ),
 CONSTRAINT "FK_143" FOREIGN KEY ( "item_id" ) REFERENCES "stock_item" ( "id" )
);

CREATE INDEX "fkIdx_140" ON "order_items"
(
 "order_id"
);

CREATE INDEX "fkIdx_143" ON "order_items"
(
 "item_id"
);