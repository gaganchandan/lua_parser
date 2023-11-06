-- Take two numbers as input and print greater number 

print("Enter first number: ")
local num1 = io.read("*n")
print("Enter second number: ")
local num2 = io.read("*n")

if num1 > num2 then
    print(num1 .. " is greater than " .. num2)
elseif num1 < num2 then
    print(num2 .. " is greater than " .. num1)
else
    print(num1 .. " is equal to " .. num2)
end
