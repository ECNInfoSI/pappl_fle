
package com.example;

import java.util.Scanner;

/**
 * Représente un personnage avec un nom et un âge.
 * Cette classe permet de stocker les informations d'un personnage
 * et de les renseigner via des saisies utilisateur.
 *
 * @author Maxence SCHWERER et Corentin GODARD
 * @version 1.0
 */
public class Personnage {

    private String nom;
    private int age;

    /**
     * Construit un personnage avec un nom et un âge définis.
     *
     * @param nom le nom du personnage
     * @param age l'âge du personnage
     */
    public Personnage(String nom, int age) {
        this.nom = nom;
        this.age = age;
    }

    /**
     * Construit un personnage sans initialisation préalable.
     */
    public Personnage() {

    }

    /**
     * Retourne le nom du personnage.
     *
     * @return le nom du personnage
     */
    public String getNom() {
        return nom;
    }

    /**
     * Modifie le nom du personnage.
     *
     * @param nom le nouveau nom du personnage
     */
    public void setNom(String nom) {
        this.nom = nom;
    }

    /**
     * Retourne l'âge du personnage.
     *
     * @return l'âge du personnage
     */
    public int getAge() {
        return age;
    }

    /**
     * Modifie l'âge du personnage.
     *
     * @param age le nouvel âge du personnage
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * Demande à l'utilisateur d'entrer l'âge du personnage.
     * Cette méthode convertit directement la saisie en entier et permet de mettre en avant une erreur si la saisie n'est pas un nombre valide.
     */
    public void demander() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Entrez votre âge : ");
        String saisie = scanner.nextLine();
        int age = Integer.parseInt(saisie);
        this.setAge(age);
        System.out.println("Personnage créé avec " + age + " ans.");
    }

    /**
     * Demande à l'utilisateur d'entrer l'âge du personnage.
     * Si la saisie n'est pas un nombre valide, un message d'erreur est affiché, en utilisant un try/catch.
     */
    public void demander_catch() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Entrez votre âge : ");
        String saisie = scanner.nextLine();
        try {
            int age = Integer.parseInt(saisie);
            this.setAge(age);
            System.out.println("Personnage créé avec " + age + " ans.");
        } catch (NumberFormatException e) {
            System.out.println("Erreur : Veuillez entrer un nombre valide pour l'âge.");
        }
    }

    /**
     * Demande à l'utilisateur d'entrer l'âge du personnage.
     *
     * @throws NumberFormatException si la valeur saisie n'est pas un entier valide
     */
    public void demander_throws() throws NumberFormatException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Entrez votre âge : ");
        String saisie = scanner.nextLine();
        int age = Integer.parseInt(saisie);
        this.setAge(age);
        System.out.println("Personnage créé avec " + age + " ans.");
    }

}