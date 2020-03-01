create or replace package pack1 is
  type zaznam is record(name phones.name%type, phone phones.phone%type);
  type kolekce is table of zaznam index by pls_integer;
  procedure vloz(co in kolekce);
end;
/
create or replace package body pack1 is
  procedure vloz(co in kolekce) is
  begin
    forall i in indices of co 
      insert into phones values(co(i).name,co(i).phone); 
  end;
end;
/
