# ---------------------------------------------------------------------------
# Copyright 2017-2018  OMRON Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from p2def import *

gender_dic = {GENDER_UNKNOWN:"-",\
              GENDER_FEMALE :"Female",\
              GENDER_MALE   :"Male"}

exp_dic = {EXP_UNKNOWN  :"-",\
           EXP_NEUTRAL  :"Neutral",\
           EXP_HAPPINESS:"Happiness",\
           EXP_SURPRISE :"Surprise",\
           EXP_ANGER    :"Anger",\
           EXP_SADNESS  :"Sadness"}

class DetectionResult(object):
    """General purpose detection result"""
    __slots__ = ['pos_x', 'pos_y', 'size', 'conf']
    def __init__(self, pos_x=None, pos_y=None, size=None, conf=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.conf = conf

    def __str__(self):
        x = self.pos_x
        y = self.pos_y
        size = self.size
        conf = self.conf
        return f'X: {x} Y: {y} Size: {size} Conf: {conf}'

class FaceResult(DetectionResult):
    """Detection result for face"""
    __slots__ = ['direction','age','gender','gaze','blink','expression','recognition']
    def __init__(self, pos_x=None, pos_y=None, size=None, conf=None):
        DetectionResult.__init__(self,pos_x,pos_y,size,conf)
        self.direction = None
        self.age = None
        self.gender = None
        self.gaze = None
        self.blink = None
        self.expression = None
        self.recognition = None

    def __str__(self):
        s = DetectionResult.__str__(self) +'\n'
        if self.direction is not None:    s += f'\t\t{str(self.direction)}\n'
        if self.age is not None:    s += f'\t\t{str(self.age)}\n'
        if self.gender is not None: s += f'\t\t{str(self.gender)}\n'
        if self.gaze is not None:   s += f'\t\t{str(self.gaze)}\n'
        if self.blink is not None:  s += f'\t\t{str(self.blink)}\n'
        if self.expression is not None:    s += f'\t\t{str(self.expression)}\n'
        if self.recognition is not None:  s += f'\t\t{str(self.recognition)}\n'
        return s

class DirectionResult(object):
    """Result for Facial direction estimation"""
    __slots__ = ['LR', 'UD', 'roll', 'conf']
    def __init__(self, LR=None, UD=None, roll=None, conf=None):
        self.LR = LR
        self.UD = UD
        self.roll = roll
        self.conf = conf

    def __str__(self):
        return f'Direction     LR: {self.LR} UD: {self.UD} Roll: {self.roll} Conf: {self.conf}'

class AgeResult(object):
    """Result of Age estimation"""
    __slots__ = ['age','conf']
    def __init__(self, age=None, conf=None):
        self.age = age
        self.conf = conf

    def __str__(self):
        string = 'Age           '
        if self.age == EST_NOT_POSSIBLE:
            string += 'Age:- '
        else:
            string += f'Age: {self.age} '
        return string + f'Conf: {self.conf}'

class GenderResult(object):
    """Result of Gender estimation"""
    __slots__ = ['gender', 'conf']
    def __init__(self, gender=None, conf=None):
        self.gender = gender
        self.conf = conf

    def __str__(self):
        if self.gender == EST_NOT_POSSIBLE:
            _dic_key = GENDER_UNKNOWN
        else:
            _dic_key = self.gender
        return f'Gender        Gender: {gender_dic[_dic_key]} Conf: {self.conf}'

class GazeResult(object):
    """Result of Gaze estimation"""
    __slots__ = ['gazeLR','gazeUD']
    def __init__(self, gazeLR=None, gazeUD=None):
        self.gazeLR = gazeLR
        self.gazeUD = gazeUD

    def __str__(self):
        return f'Gaze          LR: {self.gazeLR} UD: {self.gazeUD}'

class BlinkResult(object):
    """Result of Blink estimation"""
    __slots__ = ['ratioR','ratioL']
    def __init__(self, ratioR=None, ratioL=None):
        self.ratioR = ratioR
        self.ratioL = ratioL

    def __str__(self):
        return 'Blink         R: {self.ratioR} L: {self.ratioL}'

class ExpressionResult(object):
    """Result of Expression estimation"""
    __slots__ = ['neutral','happiness','surprise','anger','sadness','neg_pos']
    def __init__(self, neutral=None, happiness=None, surprise=None,\
                       anger=None, sadness=None, neg_pos=None, degree=None):
        self.neutral = neutral
        self.happiness = happiness
        self.surprise = surprise
        self.anger = anger
        self.sadness = sadness
        self.neg_pos = neg_pos

    def get_top1(self):
        x = [self.neutral, self.happiness, self.surprise, self.anger, self.sadness]

        max_score = max(x)
        if max_score == EST_NOT_POSSIBLE:
            max_idx = EXP_UNKNOWN
        else:
            max_idx = x.index(max_score)

        exp_str = exp_dic[max_idx]
        return exp_str, max_score

    def __str__(self):
        string ='Expression    '
        if self.neutral == EST_NOT_POSSIBLE:
            string += 'Exp:- Score:- (Neutral:- Happiness:- Surprise:- Anger:- Sadness:- NegPos:-)'
        else:
            top1_exp, top1_score = self.get_top1()
            string += f'Exp: {top1_exp} Score: {top1_score} (Neutral: {self.neutral} Happiness: {self.happiness} Surprise: {self.surprise} Anger: {self.anger} Sadness: {self.sadness} NegPos: {self.neg_pos})' 
        return string

class RecognitionResult(object):
    """Result of Recognition"""
    __slots__ = ['uid','score']
    def __init__(self, uid=None, score=None):
        self.uid = uid
        self.score = score

    def __str__(self):
        if self.uid == RECOG_NO_DATA_IN_ALBUM:
            string = 'Recognition   No data is registered in the album.'
        elif self.uid == RECOG_NOT_POSSIBLE:
            string = f'Recognition   Uid:- Score: {self.score}'
        elif self.uid == -1:
            string = f'Recognition   Uid:Unknown Score: {self.score}'
        else:
            string = f'Recognition   Uid: {self.uid} Score: {self.score}'
        return string

if __name__ == '__main__':
    pass
