# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:35:43 2019

@author: Ganesh
"""

import cricpy.analytics as ca
#ca.teamWinLossStatusAtGrounds("indiaTest.csv",teamName="India",opposition=["Australia"],homeOrAway=["all"],matchType="Test",plot=True)
ca.teamWinLossStatusVsOpposition("indiaTest.csv",teamName="India",opposition=["all"],homeOrAway=["all"],matchType="Test",plot=True)