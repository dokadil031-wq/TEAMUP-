package com.example

data class MatchEntity(
    var id: String = "",
    val category: String = "",
    val sport: String = "",
    val title: String = "",
    val location: String = "",
    val time: String = "",
    val joined: Int = 0,
    val total: Int = 0,
    val audience: String = "",
    val posterName: String = "",
    val posterId: String = "",
    val posterTrust: Double = 0.0
)
