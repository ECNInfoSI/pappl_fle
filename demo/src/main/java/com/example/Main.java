package com.example;

import java.util.LinkedList;

public class Main {
    public static void main(String[] args) {

        //java.lang.NullPointerException
        String name=null;
        System.out.println(name.length());


        //java.lang.IndexOutOfBoundsException
        LinkedList<String> list = new LinkedList<>();
        list.add("Hello");
        System.out.println(list.get(0));
        System.out.println(list.get(1));

        //ArithmeticException


    }
}